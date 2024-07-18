class UserEmailAlreadyExistsError(Exception):
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)


class UsernameAlreadyExistsError(Exception):
    def __init__(self, message="Username already exists"):
        self.message = message
        super().__init__(self.message)
