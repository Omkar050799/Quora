from django.template.loader import render_to_string
from utility.utils import send_common_email
from utility.constants import COMPANY_ADMIN_ROLE, EMPLOYEE_ROLE
from quora.tasks import app


@app.task
def send_welcome_email(email, name, role, company_name):
    """Send a welcome email based on the user role."""
    try:
        if role == COMPANY_ADMIN_ROLE:
            subject = "Welcome! Your Company is Registered"
            role_message = "Your company has been successfully registered in our system."
        elif role == EMPLOYEE_ROLE:
            subject = "Welcome to the Team!"
            role_message = "Your account has been created in the system."
        else:
            subject = "Welcome!"
            role_message = "Your account is now active."
        context = {
            "name": name,
            "company_name": company_name,
            "role": role,
            "email":email,
            "role_message": role_message
        }
        message = render_to_string("emails/welcome_email.html", context)

        # Send email asynchronously
        send_common_email.apply_async(args=[subject, message, [email], []] )
        
        # send_common_email(subject, message, [email], [])

        print("Mail sent...")
    except Exception as e:
        print("Exception : ", str(e))
        return False
