# We define exception classes here. When there is an error you want to handle,
# add an exception here without hesitation.


class ApiError(Exception):
    error_code = 0
    message = ""

    def __init__(self, message=""):
        self.message = message

    @property
    def data(self):
        return {
                'status': {
                    'code': self.error_code,
                    'message': self.message,
                }
            }

################################################################################
# Define Exceptions Here


class AtLeastOneOfArguments(ApiError):
    error_code = 1

    def __init__(self, args):
        self.message = 'At least one of {} should be provided'.format(
                ", ".join(args))


class CredentialNotFound(ApiError):
    error_code = 2

    def __init__(self, cred_type, cred_value):
        self.message = 'Credential ({}) {} is not valid'.format(
                cred_type, cred_value)


class PasswordIncorrect(ApiError):
    error_code = 3

    def __init__(self):
        self.message = "Password is incorrect"


class AccountAlreadyExists(ApiError):
    error_code = 4

    def __init__(self):
        self.message = "Account information is duplicated"


class UserInfoNotFound(ApiError):
    error_code = 5

    def __init__(self, reason=""):
        self.message = "User info can't be found"
        if reason:
            self.message += ": " + reason


class AdmissionInfoNotFound(ApiError):
    error_code = 6

    def __init__(self, reason=""):
        self.message = "Admission info can't be found"
        if reason:
            self.message += ": " + reason
