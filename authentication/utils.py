import random
from .models import CustomUser
# from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(random.randint(100000,999999))
    otp = ''
    for _ in range(6):
        otp += str(random.randint(1,9))
    return otp

 
def send_otp(email):
    otp = generate_otp()
    subject = 'OTP for Email Verification'
    user = CustomUser.objects.get(email=email)
    from_site = 'rms.com'
    email_body = f'Hi, {user.first_name} thank you for signning up on {from_site}. Your otp fro email verification is {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    print(from_email)

    send_mail(subject, email_body, from_email, [email], fail_silently=False)


    # email_data = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    # email_data.send()