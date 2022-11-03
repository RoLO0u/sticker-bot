from time import monotonic
from typing import Any, Awaitable, Callable, Dict, List

from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from templates.markups import captcha_inline
from templates.database import reg_user
from templates.mongo import MongoStorage

class AntiFloodMiddleware(BaseMiddleware):

    def __init__(self) -> None:
        super().__init__()
    
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:

        user_id = str(event.from_user.id)
        time = monotonic()

        my_storage: MongoStorage = data.get("storage")

        user_storage: Dict[str, List[bool, int]] = await my_storage.get_data(user=user_id)

        data["user_id"] = user_id
        data["user_lang"] = reg_user(user_id)

        # print(user_storage, 0)

        if not user_storage:
            user_storage["data"] = [time, False]
        elif user_storage["data"][1]:
            return
        elif user_storage["data"][0] + .5 > time: # new message sent less than in 0.5 sec
            user_storage["data"] = [time, True]
            await my_storage.set_data(user=user_id, data=user_storage)
            await event.answer("Spam catched. Complete captha to continue", reply_markup=captcha_inline())
            return
        else:
            user_storage["data"][0] = time

        # print(user_storage, 1)
        
        await my_storage.set_data(user=user_id, data=user_storage)

        return await handler(event, data)