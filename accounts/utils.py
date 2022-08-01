# External Import
import os
from .token_generator import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from dotenv import load_dotenv  # for python-dotenv method
load_dotenv()

# Internal Import


def send_email_verification(current_site, user):
    email_subject = 'Activate Your Account'
    message = render_to_string('accounts/activate_account.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    # email = EmailMessage(email_subject, message, to=[user.email])
    # email.send()

    send_mail(
        email_subject,
        message,
        os.environ.get('EMAIL'),
        [user.email],
        fail_silently=False,
    )


def send_email_to_user(email_subject, message, user):
    send_mail(
        email_subject,
        message,
        os.environ.get('EMAIL'),
        [user.email],
        fail_silently=False,
    )
