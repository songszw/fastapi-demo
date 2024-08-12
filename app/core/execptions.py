class UserEmailAlreadyExistsError(Exception):
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)


class UsernameAlreadyExistsError(Exception):
    def __init__(self, message="Username already exists"):
        self.message = message
        super().__init__(self.message)


class LoginError(Exception):
    def __init__(self, message="Incorrect username or password"):
        self.message = message
        super().__init__(self.message)


class CategoryAlreadyExistsError(Exception):
    def __init__(self, message="Category already exists"):
        self.message = message
        super().__init__(self.message)


class CategoryNotFoundError(Exception):
    def __init__(self, message="Category not found"):
        self.message = message
        super().__init__(self.message)
        

class CategoryDeleteError(Exception):
    def __init__(self, message="Category delete error"):
        self.message = message
        super().__init__(self.message)


class EntryNotFoundError(Exception):
    def __init__(self, message="Entry not found"):
        self.message = message
        super().__init__(self.message)


class CustomException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


class PasswordError(Exception):
    def __init__(self, message="Current password is incorrect"):
        self.message = message
        super().__init__(self.message)
