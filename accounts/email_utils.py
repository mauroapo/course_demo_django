"""
Email utility using Resend API for sending emails.
"""
import resend
from django.conf import settings


def send_verification_email(to_email, code, purpose='password_reset'):
    """
    Send verification code email using Resend.
    
    Args:
        to_email: Recipient email address
        code: 6-digit verification code
        purpose: 'password_reset' or 'email_change'
    """
    resend.api_key = getattr(settings, 'RESEND_API_KEY', '')
    
    if not resend.api_key:
        # Fallback to console for development
        print(f"\n{'='*60}")
        print(f"EMAIL TO: {to_email}")
        print(f"PURPOSE: {purpose}")
        print(f"VERIFICATION CODE: {code}")
        print(f"{'='*60}\n")
        return
    
    # Subject and title based on purpose
    if purpose == 'password_reset':
        subject = 'Código de Verificação - Redefinir Senha'
        title = 'Redefinir Senha'
        message = 'Você solicitou a redefinição de senha. Use o código abaixo para continuar:'
    else:  # email_change
        subject = 'Código de Verificação - Alteração de Email'
        title = 'Alteração de Email'
        message = 'Você solicitou a alteração do seu email. Use o código abaixo para confirmar:'
    
    # HTML email with inline styling
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f3f4f6;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #6B46C1, #F97316); padding: 40px 30px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: bold;">{title}</h1>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px; background-color: #f9fafb;">
                                <p style="font-size: 16px; color: #374151; margin: 0 0 20px 0;">Olá,</p>
                                
                                <p style="font-size: 16px; color: #374151; margin: 0 0 30px 0; line-height: 1.5;">
                                    {message}
                                </p>
                                
                                <!-- Code Box -->
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td align="center" style="padding: 20px; background-color: #ffffff; border-radius: 8px;">
                                            <div style="font-size: 36px; font-weight: bold; color: #6B46C1; letter-spacing: 12px; font-family: 'Courier New', monospace;">
                                                {code}
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="font-size: 14px; color: #6b7280; margin: 20px 0 0 0;">
                                    Este código expira em 10 minutos.
                                </p>
                                
                                <p style="font-size: 14px; color: #6b7280; margin: 10px 0 0 0;">
                                    Se você não solicitou esta ação, ignore este email.
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 20px 30px; text-align: center; background-color: #ffffff; border-top: 1px solid #e5e7eb;">
                                <p style="font-size: 12px; color: #9ca3af; margin: 0;">
                                    Plataforma de Cursos - Invisibilidown
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    try:
        params = {
            "from": getattr(settings, 'RESEND_FROM_EMAIL', 'onboarding@resend.dev'),
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        }
        
        email = resend.Emails.send(params)
        print(f"Email sent successfully via Resend to {to_email}")
        return email
        
    except Exception as e:
        print(f"Error sending email via Resend: {e}")
        # Fallback to console
        print(f"\n{'='*60}")
        print(f"EMAIL TO: {to_email}")
        print(f"SUBJECT: {subject}")
        print(f"VERIFICATION CODE: {code}")
        print(f"{'='*60}\n")
        return None
