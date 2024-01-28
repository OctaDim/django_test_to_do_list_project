STATUS_NAME_LEN_ERROR_MESSAGE = "The Status name length should be between 3-30"
CATEGORY_NAME_LEN_ERROR_MESSAGE = "The Category name length should be between 4-25"

PASSWORDS_DO_NOT_MATCH_ERROR = "Passwords do not match. Please, try again"
PASSWORD_REQUIRED_MESSAGE = "Empty password. Password is required"

USERNAME_ALREADY_EXISTS = "Such username already exists. Try another username"
EMAIL_ALREADY_EXISTS = "Such email already exists. Try another email"

NON_VALID_EMAIL_MESSAGE = "Please, enter a valid email"

EMAIL_REQUIRED_MESSAGE = "Empty email. Email is required"
EMAIL_OR_USERNAME_REQUIRED_MESSAGE = "Empty login name. Email or Username is required"

FIRST_NAME_REQUIRED_MESSAGE = "Empty first name. First name is required"
LAST_NAME_REQUIRED_MESSAGE = "Empty last name. Last name is required"

NOT_IS_STAFF_ERROR = "Admin must be staff"
NOT_IS_SUPERUSER_ERROR = "Admin must be a superuser"


def USER_NOT_FOUND_MESSAGE(email: str) -> str:
    return f"User with email {email} was not found"
