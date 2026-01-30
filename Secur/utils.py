from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
# from .models import *
import random
from django.conf import settings


def send_notification_to_user(user_id, notification_type, message, created_at):
    print(f"DEBUG 4: Sending to user {user_id}, room: notifications_{user_id}")
    
    channel_layer = get_channel_layer()
    print(f"DEBUG 5: Channel layer: {channel_layer}")
    
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user_id}",
        {
            'type': 'notification_message',
            'notification_type': notification_type,
            'message': message,
            'created_at': str(created_at),
        }
    )
    
    print("DEBUG 6: group_send completed")

def otp_verification(user, email):
    from .models import OTPVerification

    ten_minutes = timezone.now()  - timedelta(minutes=10)
    existing_otp = OTPVerification.objects.filter(
        user_verification = user,
        email = email,
        created_at__gte = ten_minutes,
        is_used = False
    )
    if existing_otp.exists():
        otp_object = existing_otp.first()
    else:
        otp_code = random.randint(100000, 999999)
        otp_object = OTPVerification.objects.create(
            user_verification = user,
            email = email,
            otp_code=otp_code
        )
        send_mail(
            subject="Email Verification for User",
            message=f"Here is the otp code for {email} and your code is {otp_object.otp_code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
    return otp_object
