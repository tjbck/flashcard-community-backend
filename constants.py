from enum import Enum


class MESSAGES(str, Enum):
    DEFAULT = lambda msg="": f"{msg if msg else ''}"


class ERROR_MESSAGES(str, Enum):
    def __str__(self) -> str:
        return super().__str__()

    DEFAULT = lambda err="": f"Something went wrong :/\n{err if err else ''}"
    ENV_VAR_NOT_FOUND = "Required environment variable not found. Terminating now."
    INVALID_TOKEN = (
        "Your session has expired or the token is invalid. Please sign in again."
    )
    EMAIL_TAKEN = "Uh-oh! This email is already registered. Sign in with your existing account or choose another email to start anew."
    USERNAME_TAKEN = (
        "Uh-oh! This username is already registered. Please choose another username."
    )
    TAGNAME_TAKEN = "Uh-oh! This model tag name is already being used. Please choose another tag name."
    INVALID_TAGNAME = (
        lambda err="": f"Uh-oh! This model tag name cannot be used{f' {err}' if err else ''}. Please choose another tag name."
    )

    INVALID_CRED = "The email or password provided is incorrect. Please check for typos and try logging in again."
    UNAUTHORIZED = "401 Unauthorized"
    ACCESS_PROHIBITED = "You do not have permission to access this resource. Please contact your administrator for assistance."
    ACTION_PROHIBITED = (
        "The requested action has been restricted as a security measure."
    )
    USER_NOT_FOUND = "We could not find what you're looking for :/"
    NOT_FOUND = "We could not find what you're looking for :/"
    MALICIOUS = "Unusual activities detected, please try again in a few minutes."
