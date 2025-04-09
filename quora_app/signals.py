from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from utility.signals_utility import send_welcome_email

User = get_user_model()

# @receiver(post_save, sender=User)
# def send_welcome_email_signal(sender, instance, created, **kwargs):
#     """Trigger welcome email after user creation."""
#     if created:
#         # Extract only the necessary user data
#         user_data = {
#             'email': instance.email,
#             'first_name': instance.first_name,
#             'role_id': instance.role_id,
#             'company_name': instance.company.company_name if hasattr(instance, 'company') else None
#         }
        
#         # Send welcome email with the extracted data
#         send_welcome_email.apply_async(
#             args=[user_data['email'], user_data['first_name'], user_data['role_id'], user_data['company_name']]
#         )
