from typing import Any
from time import monotonic

from aiogram import Router, F, types
from aiogram.types import CallbackQuery

from templates.database.fsm.mongo import MongoStorage
from templates import const

router = Router()

@router.callback_query(F.data.startswith("spam"))
async def callback_query_handler(callback_query: CallbackQuery, storage: MongoStorage) -> None:

    assert callback_query.data and isinstance(callback_query.message, types.Message)

    user_id = str(callback_query.from_user.id)
    user_storage = await storage.get_data(user=user_id)

    if int(callback_query.data[4:]) == user_storage["data"][2]:
        time = monotonic()
        await callback_query.message.answer(const.CAPTCHA_COMPLETED)
        user_storage["data"] = [time, False, 0]
        await storage.set_data(user=user_id, data=user_storage)
        await callback_query.message.delete()