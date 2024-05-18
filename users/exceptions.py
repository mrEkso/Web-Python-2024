class UserNotFound(Exception):
    """Exception raised when user is not found."""

    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)


class EmailAlreadyExists(Exception):
    """Exception raised when the email is already in use."""

    def __init__(self, message="Email already in use"):
        self.message = message
        super().__init__(self.message)
