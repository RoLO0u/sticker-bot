class TokenDoesNotDefined(Exception):

    def __init__(self, message="Token does not defined"):
        self.message = message
        super().__init__(self.message)

class InvalidEnvException(Exception):
    
    def __init__(self, message="Bot username (BOT_NAME) does not defined") -> None:
        self.message = message
        super().__init__(self.message)