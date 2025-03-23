from aiogram.types.error_event import ErrorEvent

class UserException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
        
    @classmethod
    def isinstance(cls, exception: ErrorEvent) -> bool:
        return isinstance(exception.exception, cls)

class TokenIsNotDefined(UserException):
    def __init__(self,
            message="Token is not defined"
        ) -> None:
        self.message = message
        super().__init__(self.message)

class InvalidEnvException(UserException):
    def __init__(self,
            message: str = "Bot username (BOT_NAME)"
        ) -> None:
        self.message = f"{message} is not defined"
        super().__init__(self.message)
        
class NotFoundException(UserException):
    def __init__(self, object="user") -> None:
        self.message = f"\"{object=}\" is not found"
        super().__init__(self.message)
        
class WatermarkIsNotDefined(Exception):
    def __init__(self,
            message: str = "Watermark is not set"
        ) -> None:
        self.message = message
        super().__init__(self.message)