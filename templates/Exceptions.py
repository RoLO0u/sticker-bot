class TokenDoesNotDefined(Exception):

    def __init__(self, message="Token does not defined"):
        self.message = message
        super().__init__(self.message)