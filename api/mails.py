from django.core.mail import send_mail
import random
from django.conf import settings
from api.models import User

def send_otp_via_email(email):
    subject = 'OTP for your account'
    otp = random.randint(1000,9999)
    massage = f'Your OTP is {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, massage, 'mo.umar6628@gmail.com', [email])
    user_object = User.objects.get(email=email)
    user_object.otp = otp
    user_object.save()