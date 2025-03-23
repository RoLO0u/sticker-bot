from aiogram import Router, F
from aiogram.types.error_event import ErrorEvent
from templates import Exceptions, throttling
from templates.types import texts

router = Router()
router.errors.middleware(throttling.ErrorsMiddleware())
    
@router.errors()
async def any_exception(exception: ErrorEvent, user_lang: str) -> None:
    assert exception.update.message
    await exception.update.message.answer(texts["unknown_exception_1"][user_lang]+"404")
    raise exception.exception