OTP_EXPIRE_MINUTE_TIME = 15

STATUS_ACTIVE = 1
STATUS_INACTIVE = 2
STATUS_DELETED = 3

SUPER_ADMIN_ROLE = 1

FEMALE = 2
MALE = 1
OTHER = 3

SUPERUSER_ROLE = 1
COMPANY_ADMIN_ROLE = 2
EMPLOYEE_ROLE = 3
ROLE_CHOICES = [SUPERUSER_ROLE, COMPANY_ADMIN_ROLE, EMPLOYEE_ROLE]

EMPLOYEE_ROLES = []

STAFF = 2

BASE_URL = 'http://127.0.0.1:8000/api/v1/'
ACCESS_KEY = "AE698wLwHGPLvtuzF46V4P2h4yh3ru2MmkBKpsEA7bzQSHjQ3F"

MESSAGES = {
    "username_password_required": "Username and password are required. ",
    "invalid_username_and_password": "Invalid username or password. Please try again.",
    "email_not_provided": "Email not provided.",
    "forget_password_email_subject": "Stark Employee Portal reset Password",
    "send_email_otp_email_subject": "OTP for email verification",
    "password_confirm_password_invalid": "Password and confirm password does not match.",
    "created": " created successfully.",
    "updated": " updated successfully.",
    "deleted": " deleted successfully.",
    "not_found": " not found.",
    "email_not_exist":"Email not exists.",
    "username_not_exist":"Username not exists.",
    "user_inactive":"User is inactive.",
    "user_deleted":"User is deleted.",
    "invalid_mobile_number": "Invalid mobile number",
    "all_fields_are_required": "All fields should not be empty."
}

FORGET_PASSWORD_TOKEN_EXPIRY_IN_SEC = 24 * 60 * 60

BYTES_PER_MB = 1073741824
FILE_SIZE = 5

APPLICATION_STARTED = 1
APPLICATION_PENDING = 2
APPLICATION_IN_PROGRESS = 3
APPLICATION_COMPLETED = 4
APPLICATION_FAILED = 5
APPLICATION_RETRY_REQUIRED = 6
APPLICATION_STATUS_CHOICES = [
    APPLICATION_STARTED, APPLICATION_PENDING, APPLICATION_IN_PROGRESS, APPLICATION_COMPLETED,
    APPLICATION_FAILED, APPLICATION_RETRY_REQUIRED
]

# providers
ACCELA = 1
ETRAKIT = 2
OPENGOV = 3
TYLERHOST = 4
OTHER = 5
AHJ_PROVIDER_CHOICES = [
    ACCELA, ETRAKIT, OPENGOV, TYLERHOST, OTHER
]

INFO = 1
WARNING = 2
ERROR = 3
DEBUG = 4

LOG_LEVELS = [INFO, WARNING, ERROR, DEBUG]
            
AHJ_APPLICATION_PENDING = 1
AHJ_APPLICATION_DRAFT = 2
AHJ_APPLICATION_SUBMITTED = 3
AHJ_APPLICATION_STATUS_CHOICES = [AHJ_APPLICATION_PENDING ,AHJ_APPLICATION_DRAFT ,AHJ_APPLICATION_SUBMITTED]
