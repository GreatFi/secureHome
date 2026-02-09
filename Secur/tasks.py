from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
import os
import resend
@shared_task
def send_property_listing_email(user_email, property_name):
    subject = f'Property Listing Confirmation - {property_name}'
    message = f'''
    Your property "{property_name}" has been submitted successfully and is currently under review.
    
    We'll notify you once it's been approved or if we need any changes.
    
    Thank you for using SecureHome!
    '''
    
    resend.api_key = os.environ.get("RESEND_API_KEY")

    resend.Emails.send({
        "from" : settings.DEFAULT_FROM_EMAIL,
        "to": [user_email],
        "subject" : f"{subject}",
        "html" : f"{message}"
    })
    
    return f'Email sent to {user_email}'

@shared_task
def send_account_created_email(user_email, username):
    subject = f"Welcome Message"
    message = f"Welcome {username} to SecureHome! Your account has been created successfully."

    resend.api_key = os.environ.get("RESEND_API_KEY")

    resend.Emails.send({
        "from" : settings.DEFAULT_FROM_EMAIL,
        "to": [user_email],
        "subject" : f"{subject}",
        "html": f"{message}"
    })

    return f"email sent to {user_email}"
@shared_task
def send_loggedin_email(user_email, username):
    subject = f"Welcome Back {username}"
    message = "You have successfully logged into your account"

    resend.api_key = os.environ.get("RESEND_API_KEY")

    resend.Emails.send({
        "from" : settings.DEFAULT_FROM_EMAIL,
        "to": [user_email],
        "subject" : f"{subject}",
        "html": f"{message}",
    })
    return f"Email sent successfully to {user_email}"

@shared_task
def send_status_update_email(user_email, property_name, status):
    subject = f'Property Status Update - {property_name}'
    message =  f"{status}"
    
    resend.api_key = os.environ.get("RESEND_API_KEY")

    resend.Emails.send({
        "from" : settings.DEFAULT_FROM_EMAIL,
        "to": [user_email],
        "subject" : f"{subject}",
        "html": f"{message}",
    })

    return f'Email sent to {user_email}'


@shared_task
def send_property_upload_email(user_email, property_name):
    subject = "Property Upload Confirmation"
    message = f"Your property {property_name} has been uploaded successfully"


    resend.api_key = os.environ.get("RESEND_API_KEY")

    resend.Emails.send({
        "from" : settings.DEFAULT_FROM_EMAIL,
        "to": [user_email],
        "subject" : f"{subject}",
        "html": f"{message}",
    })

    return f"Email sent to {user_email}"

@shared_task
def send_logout_email(user_email, username):
    subject = "Logout Notifications"
    message = f"{username} have been logged out successfully"

    resend.api_key = os.environ.get("RESEND_API_KEY")

    resend.Emails.send({
        "from" : settings.DEFAULT_FROM_EMAIL,
        "to": [user_email],
        "subject" : f"{subject}",
        "html": f"{message}",
    })

    return f"Email sent successfully to {user_email}"


