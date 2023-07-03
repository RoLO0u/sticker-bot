import logging

from time import monotonic
from typing import Any, Awaitable, Callable, Dict, Coroutine, List

from aiogram.types import Message, TelegramObject
from aiogram.types.error_event import ErrorEvent
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from templates.markups import captcha_inline
from templates.database import baseDB
from templates.database.fsm.mongo import MongoStorage
from templates.database.fsm.postgres import PostgreStorage
from templates.Exceptions import EmptyUsernameException

class AntiFloodMiddleware(BaseMiddleware):

    def __init__(self) -> None:
        super().__init__()
            
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Coroutine[Any, Any, Any] | None:
        
        assert event.from_user is not None
        
        User: baseDB.User = data["User"]
        user_id = str(event.from_user.id)
        time = monotonic()

        my_storage = data.get("storage")
        assert isinstance(my_storage, MongoStorage) or isinstance(my_storage, PostgreStorage)

        user_storage: Dict[str, List[float | bool]] = await my_storage.get_data(user=user_id)

        username = event.from_user.username
        if username is None:
            raise EmptyUsernameException
        
        data["user_id"] = user_id
        data["user_lang"] = User.register(user_id, username)

        if not user_storage or not user_storage.get("data"):
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
        
        await my_storage.set_data(user=user_id, data=user_storage)

        return await handler(event, data)
    
class ErrorsMiddleware(BaseMiddleware):
    
    def __init__(self) -> None:
        super().__init__()
        
    async def call(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: ErrorEvent, data: Dict[str, Any]) -> Coroutine[Any, Any, Any] | None:
        
        assert event.update.message is not None
        assert event.update.message.from_user is not None
    
        User: baseDB.User = data["User"]
        user_id = str(event.update.message.from_user.id)
        time = monotonic()

        my_storage = data.get("storage")
        assert isinstance(my_storage, MongoStorage) or isinstance(my_storage, PostgreStorage)

        user_storage: Dict[str, List[float | bool]] = await my_storage.get_data(user=user_id)

        username = event.update.message.from_user.username
        if username is None:
            if not EmptyUsernameException.isinstance(event):
                raise EmptyUsernameException
        
        data["user_id"] = user_id
        data["user_lang"] = User.get(user_id)['language'] if User.is_exist(user_id) else 'en'

        if not user_storage or not user_storage.get("exception_data"):
            user_storage["exception_data"] = [time, False]
        elif user_storage["exception_data"][1]:
            return
        elif user_storage["exception_data"][0] + .5 > time: # new message sent less than in 0.5 sec
            user_storage["exception_data"] = [time, True]
            await my_storage.set_data(user=user_id, data=user_storage)
            await event.update.message.answer("Spam catched. Complete captha to continue", reply_markup=captcha_inline())
            return
        else:
            user_storage["exception_data"][0] = time
        
        await my_storage.set_data(user=user_id, data=user_storage)
        
        return await handler(event, data)
        
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: ErrorEvent, data: Dict[str, Any]) -> Coroutine[Any, Any, Any] | None:
        try:
            return await self.call(handler, event, data)
        except Exception as e:
            logging.error("Error middleware exception")
            raise e