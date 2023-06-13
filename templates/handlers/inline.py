from typing import Any
from time import monotonic

from aiogram import Router, F

from aiogram.types import CallbackQuery

from templates.mongo import MongoStorage

router = Router()

@router.callback_query(F.data == "1")
async def callback_query_handler(callback_query: CallbackQuery, storage: MongoStorage) -> Any:

    user_id = str(callback_query.from_user.id)
    time = monotonic()
    assert callback_query.message is not None

    await callback_query.message.answer("You are unbanned now\nNext time be careful and don't type too fast")
    await storage.set_data(user=user_id, data={"data": [time, False]})
    await callback_query.message.delete()