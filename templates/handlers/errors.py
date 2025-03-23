from aiogram import Router, F
from aiogram.types.error_event import ErrorEvent
from templates import throttling
from templates.types import texts
from templates.database import baseDB

router = Router()
router.errors.middleware(throttling.ErrorsMiddleware())
    
@router.errors()
async def any_exception(exception: ErrorEvent, user: baseDB.User) -> None:
    assert exception.update.message
    await exception.update.message.answer(texts["unknown_exception_1"][user.lang]+"404")
    raise exception.exception