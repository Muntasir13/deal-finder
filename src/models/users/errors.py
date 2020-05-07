class UserErrors(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistError(UserErrors):
    pass


class IncorrectPasswordError(UserErrors):
    pass


class UserAlreadyExistsError(UserErrors):
    pass


class InvalidEmailFormat(UserErrors):
    pass


class NotSamePasswordError(UserErrors):
    pass


class PasswordMatchError(UserErrors):
    pass
