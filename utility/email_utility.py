import os
import base64
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.template.loader import render_to_string
from quora.tasks import app
from utility.utils import send_common_email


def generate_secure_token(text: str):
    return TimestampSigner().sign(base64.urlsafe_b64encode(text.encode()).decode())

def verify_tamper_secure_token(token, max_age=86400):
    """ Verifies the signed token and extracts the email. """
    try:
        encoded_email = TimestampSigner().unsign(token, max_age=max_age)  # Validate token within max_age 
        return base64.urlsafe_b64decode(encoded_email.encode()).decode()  # Decode email
    except SignatureExpired:
        return "expired"
    except BadSignature:
        return None

# Celery task to send a password reset email
# @app.task
def send_set_password_email(user_instance, company_instance):
    try:
        if not user_instance.email:
            return

        subject = "Set Your Password - Instapermit"
        to_email = [user_instance.email]
        cc_email = []

        # Generate secure token for password reset
        token = generate_secure_token(user_instance.email)
        set_password_link = f"{os.getenv('FRONT_END_URL')}/set-password/{token}"

        print("set_password_link : ", set_password_link)
        print("token : ", token)

        context = {
            "name": user_instance.first_name,
            "set_password_link": set_password_link,
            "company_name": company_instance.company_name,
            "role": user_instance.role_id,
        }

        # Render email template
        message = render_to_string("emails/set_password_email.html", context)

        # Send email asynchronously
        # send_common_email.apply_async(
        #     args=[subject, message, to_email, cc_email], countdown=10
        # )

        send_common_email(subject, message, to_email, cc_email)
        return True

    except Exception as e:
        print("Exception : ", str(e))
        return False
