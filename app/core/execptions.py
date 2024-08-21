class UserEmailAlreadyExistsError(Exception):
    def __init__(self, message="EMAIL_ALREADY_EXISTS"):
        self.message = message
        super().__init__(self.message)


class UsernameAlreadyExistsError(Exception):
    def __init__(self, message="USERNAME_ALREADY_EXISTS"):
        self.message = message
        super().__init__(self.message)


class LoginError(Exception):
    def __init__(self, message="INCORRECT_USERNAME_OR_PASSWORD"):
        self.message = message
        super().__init__(self.message)


class CategoryAlreadyExistsError(Exception):
    def __init__(self, message="CATEGORY_ALREADY_EXISTS"):
        self.message = message
        super().__init__(self.message)


class CategoryNotFoundError(Exception):
    def __init__(self, message="CATEGORY_NOT_FOUND"):
        self.message = message
        super().__init__(self.message)
        

class CategoryDeleteError(Exception):
    def __init__(self, message="CATEGORY_DELETE_ERROR"):
        self.message = message
        super().__init__(self.message)


class EntryNotFoundError(Exception):
    def __init__(self, message="ENTRY_NOT_FOUND"):
        self.message = message
        super().__init__(self.message)


class CustomException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


class PasswordError(Exception):
    def __init__(self, message="CURRENT_PASSWORD_IS_INCORRECT"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __init__(self, message="USER_NOT_FOUND"):
        self.message = message
        super().__init__(self.message)
