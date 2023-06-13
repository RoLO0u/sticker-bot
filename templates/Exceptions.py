from aiogram.types.error_event import ErrorEvent

class UserException(Exception):
    
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
        
    @classmethod
    def isinstance(cls, exception: ErrorEvent) -> bool:
        return isinstance(exception.exception, cls)

class TokenDoesNotDefined(UserException):

    def __init__(self, message="Token does not defined"):
        self.message = message
        super().__init__(self.message)

class InvalidEnvException(UserException):
    
    def __init__(self, message="Bot username (BOT_NAME) does not defined") -> None:
        self.message = message
        super().__init__(self.message)
        
class NotFoundException(UserException):
    
    def __init__(self, object="user") -> None:
        self.message = f"\"{object=}\" does not found"
        super().__init__(self.message)
        
class EmptyUsernameException(UserException):
    
    def __init__(self, message: str = "User doesn't have username") -> None:
        self.message = message
        super().__init__(self.message)