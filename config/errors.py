class Errors():
    DUPLICATE_USER_NAME_ERROR = BaseException("No two users may have the same username")
    DUPLICATE_EMAIL_ERROR = BaseException("No two users may have the same email")
    DUPLICATE_PHONE_ERROR = BaseException("No two users may have the same phone number")
    USER_NOT_FOUND_ERROR = BaseException("This user has not created an account")