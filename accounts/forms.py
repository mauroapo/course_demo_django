from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Profile, EmailVerificationCode

User = get_user_model()


class LoginForm(AuthenticationForm):
    """Custom login form."""
    
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'seu@email.com',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••'
        })
    )


class SignupForm(UserCreationForm):
    """Custom signup form."""
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'seu@email.com'
        })
    )
    first_name = forms.CharField(
        label='Nome',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Seu nome'
        })
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Seu sobrenome'
        })
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••'
        })
    )
    password2 = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••'
        })
    )
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    """Form for editing user profile."""
    
    date_of_birth = forms.DateField(
        label='Data de Nascimento',
        required=False,
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.DateInput(
            attrs={
                'class': 'form-input',
                'type': 'date'
            },
            format='%Y-%m-%d'
        )
    )
    nationality = forms.CharField(
        label='Nacionalidade',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ex: Brasileiro'
        })
    )
    
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'nationality')


class EmailChangeRequestForm(forms.Form):
    """Form for requesting email change."""
    
    new_email = forms.EmailField(
        label='Novo Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'novo@email.com'
        })
    )
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    
    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')
        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError('Este email já está em uso.')
        if self.user and new_email == self.user.email:
            raise forms.ValidationError('Este é o seu email atual.')
        return new_email


class EmailChangeConfirmForm(forms.Form):
    """Form for confirming email change with verification code."""
    
    code = forms.CharField(
        label='Código de Verificação',
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '000000',
            'maxlength': '6'
        })
    )
