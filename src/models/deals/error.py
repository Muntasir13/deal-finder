class DealError(Exception):
    def __init__(self, message):
        self.message = message


class FileTypeError(DealError):
    pass
