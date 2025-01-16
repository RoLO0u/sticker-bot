from typing import Any

from aiogram import Router
from aiogram.types.error_event import ErrorEvent
from templates import Exceptions, throttling
from templates.types import texts

router = Router()
router.errors.middleware(throttling.ErrorsMiddleware())

@router.errors(Exceptions.EmptyUsernameException.isinstance)
async def empty_username(exception: ErrorEvent, user_lang: str) -> None:
    assert exception.update.message
    await exception.update.message.answer(texts["uname_error"][user_lang])
    
@router.errors()
async def any_exception(exception: ErrorEvent, user_lang: str) -> None:
    assert exception.update.message
    await exception.update.message.answer(texts["unknown_exception_1"][user_lang]+"404")
    raise exception.exception