from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, SignupForm, ProfileForm, EmailChangeRequestForm, EmailChangeConfirmForm
from .models import EmailVerificationCode, PasswordResetCode, CustomUser
from . import email_utils


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def signup_view(request):
    """User signup view."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login')


@login_required
def account_view(request):
    """User account management view."""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('account')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'accounts/account.html', {
        'form': form,
        'user': request.user
    })


@login_required
def change_email_request(request):
    """Request email change with verification code."""
    if request.method == 'POST':
        form = EmailChangeRequestForm(request.POST, user=request.user)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            
            # Generate verification code
            code = EmailVerificationCode.generate_code()
            
            # Save verification code
            EmailVerificationCode.objects.create(
                user=request.user,
                new_email=new_email,
                code=code
            )
            
            # Send email with code using Resend
            email_utils.send_verification_email(
                to_email=new_email,
                code=code,
                purpose='email_change'
            )
            
            messages.success(request, f'Código de verificação enviado para {new_email}')
            return redirect('change_email_confirm')
    else:
        form = EmailChangeRequestForm(user=request.user)
    
    return render(request, 'accounts/change_email_request.html', {'form': form})


@login_required
def change_email_confirm(request):
    """Confirm email change with verification code."""
    if request.method == 'POST':
        form = EmailChangeConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            
            # Find valid verification code
            verification = EmailVerificationCode.objects.filter(
                user=request.user,
                code=code,
                is_used=False
            ).order_by('-created_at').first()
            
            if verification and verification.is_valid():
                # Update user email
                request.user.email = verification.new_email
                request.user.save()
                
                # Mark code as used
                verification.is_used = True
                verification.save()
                
                messages.success(request, 'Email alterado com sucesso!')
                return redirect('account')
            else:
                messages.error(request, 'Código inválido ou expirado.')
    else:
        form = EmailChangeConfirmForm()
    
    return render(request, 'accounts/change_email_confirm.html', {'form': form})


# ============================================================================
# PASSWORD RESET VIEWS (3-STEP FLOW)
# ============================================================================

def forgot_password_request(request):
    """Step 1: Request password reset code."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        # Check if user exists
        try:
            user = CustomUser.objects.get(email=email)
            
            # Generate verification code
            from .models import PasswordResetCode
            from .email_utils import send_verification_email
            
            code = PasswordResetCode.generate_code()
            
            # Save code
            PasswordResetCode.objects.create(
                user=user,
                code=code
            )
            
            # Send email with Resend
            send_verification_email(email, code, purpose='password_reset')
            
            # Store email in session for next step
            request.session['reset_email'] = email
            
            messages.success(request, 'Código de verificação enviado para seu email!')
            return redirect('forgot_password_verify')
            
        except CustomUser.DoesNotExist:
            # Don't reveal if email exists (security)
            request.session['reset_email'] = email
            messages.success(request, 'Se o email existir, você receberá um código de verificação.')
            return redirect('forgot_password_verify')
    
    return render(request, 'accounts/forgot_password_request.html')


def forgot_password_verify(request):
    """Step 2: Verify code."""
    if request.user.is_authenticated:
        return redirect('home')
    
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, 'Sessão expirada. Por favor, solicite um novo código.')
        return redirect('forgot_password_request')
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        
        # Find user
        try:
            user = CustomUser.objects.get(email=email)
            
            # Find valid code
            from .models import PasswordResetCode
            reset_code = PasswordResetCode.objects.filter(
                user=user,
                code=code,
                is_used=False
            ).order_by('-created_at').first()
            
            if reset_code and reset_code.is_valid():
                # Store code in session for next step
                request.session['reset_code_id'] = reset_code.id
                return redirect('forgot_password_reset')
            else:
                messages.error(request, 'Código inválido ou expirado.')
                
        except CustomUser.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
    
    # Option to resend code
    if request.GET.get('resend') == '1':
        try:
            user = CustomUser.objects.get(email=email)
            from .models import PasswordResetCode
            from .email_utils import send_verification_email
            
            code = PasswordResetCode.generate_code()
            PasswordResetCode.objects.create(user=user, code=code)
            send_verification_email(email, code, purpose='password_reset')
            
            messages.success(request, 'Novo código enviado!')
        except CustomUser.DoesNotExist:
            pass
    
    return render(request, 'accounts/forgot_password_verify.html', {'email': email})


def forgot_password_reset(request):
    """Step 3: Set new password."""
    if request.user.is_authenticated:
        return redirect('home')
    
    reset_code_id = request.session.get('reset_code_id')
    if not reset_code_id:
        messages.error(request, 'Sessão expirada. Por favor, solicite um novo código.')
        return redirect('forgot_password_request')
    
    # Get reset code
    from .models import PasswordResetCode
    try:
        reset_code = PasswordResetCode.objects.get(id=reset_code_id)
        
        # Double-check validity
        if not reset_code.is_valid() or reset_code.is_used:
            messages.error(request, 'Código expirado. Por favor, solicite um novo.')
            return redirect('forgot_password_request')
        
    except PasswordResetCode.DoesNotExist:
        messages.error(request, 'Código inválido.')
        return redirect('forgot_password_request')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validate passwords
        if not password or len(password) < 8:
            messages.error(request, 'A senha deve ter pelo menos 8 caracteres.')
        elif password != password_confirm:
            messages.error(request, 'As senhas não coincidem.')
        else:
            # Update password
            user = reset_code.user
            user.set_password(password)
            user.save()
            
            # Mark code as used
            reset_code.is_used = True
            reset_code.save()
            
            # Clear session
            request.session.pop('reset_email', None)
            request.session.pop('reset_code_id', None)
            
            messages.success(request, 'Senha redefinida com sucesso! Faça login com sua nova senha.')
            return redirect('login')
    
    return render(request, 'accounts/forgot_password_reset.html', {
        'user_email': reset_code.user.email
    })
