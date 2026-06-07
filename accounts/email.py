from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_otp_email(to_email: str, otp: str, name: str) -> bool:
    """
    Sends OTP email via Django's email backend.
    Returns True on success, False on failure.
    """
    subject = f"Your AnimeShop verification code: {otp}"
    from_email = settings.DEFAULT_FROM_EMAIL

    text_body = (
        f"Hi {name},\n\n"
        f"Your AnimeShop verification code is {otp}.\n"
        "It expires in 10 minutes.\n\n"
        "If you did not request this code, please ignore this email."
    )

    html_body = f"""
    <div style="background:#0a0a0a;color:#f0ece0;padding:24px;font-family:Arial,sans-serif;">
      <div style="max-width:560px;margin:0 auto;border:4px solid #cc1a1a;padding:20px;background:#111;">
        <h2 style="margin:0 0 12px 0;color:#c9a84c;">AnimeShop Verification</h2>
        <p style="margin:0 0 12px 0;">Hi {name},</p>
        <p style="margin:0 0 12px 0;">Use the code below to complete your registration:</p>
        <div style="font-size:28px;font-weight:bold;letter-spacing:6px;background:#cc1a1a;color:#fff;padding:12px 16px;display:inline-block;border-radius:4px;">
          {otp}
        </div>
        <p style="margin:16px 0 0 0;font-size:14px;">This code expires in 10 minutes.</p>
        <p style="margin:8px 0 0 0;font-size:12px;opacity:0.8;">If you did not request this code, you can safely ignore this email.</p>
      </div>
    </div>
    """

    try:
        msg = EmailMultiAlternatives(subject, text_body, from_email, [to_email])
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        return True
    except Exception:
        return False
