class BaseError(Exception):

    message = ''

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return str(self.message)
