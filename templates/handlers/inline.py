from typing import Any
from time import monotonic

from aiogram import Router, F, types
from aiogram.fsm.storage import base

from templates import const

router = Router()

@router.callback_query(F.data.startswith("spam"), F.chat.type=="private")
async def callback_query_handler(callback_query: types.CallbackQuery, storage: base.BaseStorage) -> None:

    assert callback_query.data and isinstance(callback_query.message, types.Message)
    assert callback_query._bot
    key = base.StorageKey(bot_id=callback_query._bot.id, chat_id=callback_query.message.chat.id, user_id=callback_query.from_user.id)

    user_storage = await storage.get_data(key)

    if int(callback_query.data[4:]) == user_storage["data"][2]:
        time = monotonic()
        await callback_query.message.answer(const.CAPTCHA_COMPLETED)
        user_storage["data"] = [time, False, 0]
        await storage.set_data(key, user_storage)
        await callback_query.message.delete()