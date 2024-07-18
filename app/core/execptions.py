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
