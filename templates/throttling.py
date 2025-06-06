import logging

from time import time as timeSeconds
from typing import Any, Awaitable, Callable, Dict, Coroutine, List, Type

from aiogram import Bot
from aiogram.types import Message, TelegramObject, BufferedInputFile, CallbackQuery
from aiogram.types.error_event import ErrorEvent
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.fsm.storage.base import StorageKey, BaseStorage

from templates.markups import captcha_inline
from templates.database import baseDB
from templates.images import create_captcha
from templates import const

class AntiFloodMiddleware(BaseMiddleware):
            
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]) -> Coroutine[Any, Any, Any] | None:
        
        if isinstance(event, CallbackQuery):
            message = event.message
            assert message
            chat_id = message.chat.id
        elif isinstance(event, Message):
            chat_id = event.chat.id
            message = event
        else: return

        assert event.from_user

        bot: Bot = data["bot"]
        User: Type[baseDB.User] = data["User"]
        user_id = str(event.from_user.id)
        time = timeSeconds()

        my_storage = data.get("storage")
        assert isinstance(my_storage, BaseStorage)

        key = StorageKey(bot_id=bot.id, chat_id=chat_id, user_id=event.from_user.id)
        user_storage: Dict[str, List[float | bool | int]] = await my_storage.get_data(key)

        username = event.from_user.username
        first_name = event.from_user.first_name

        data["user_lang"] = User.register(user_id, username, first_name)
        user = User(user_id)
        data["user"] = user

        if not user_storage or not user_storage.get("data"):
            user_storage["data"] = [time, False, 0]
        elif user_storage["data"][1]:
            if isinstance(event, CallbackQuery) and event.data and event.data[:4] == "spam":
                pass
            else: return
        elif isinstance(event, Message) and event.photo:
            pass
        elif user_storage["data"][0] + .5 > time: # new message sent less than in 0.5 sec
            image, angle = create_captcha()
            user_storage["data"] = [time, True, angle]
            await my_storage.set_data(key, user_storage)
            await message.answer_photo(BufferedInputFile(image, filename="captcha"),
                const.SPAM_CATCHED, reply_markup=captcha_inline())
            return
        else:
            user_storage["data"][0] = time
        
        await my_storage.set_data(key, user_storage)

        if chosen := user.get_chosen():
            if isinstance(message, Message) and message.text == "/start":
                return await handler(event, data)
            elif not user.id in chosen["members"]:
                await message.answer(data["texts"]["not_in_pack_e"][user.lang].format(chosen["title"]))
                return

        return await handler(event, data)
class ErrorsMiddleware(BaseMiddleware):
        
    async def call(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: ErrorEvent, data: Dict[str, Any]) -> Coroutine[Any, Any, Any] | None:

        if event.update.callback_query is not None:
            logging.error(f"Exception with callback_query update.\nevent is:\n{event}")
            logging.error(f"The exception is {event.exception}")
            raise event.exception
        
        # When message is spam was handled some time ago
        # telegram will throw an error for trying to delete
        # old message. Assertion below also throws error because
        # event.update.message is None, not types.Message
        # TODO: test and create edge case for old spams
        if event.update.message is None:
            logging.error(f"event.update.message is None\nevent is:\n{event}")
            return

        if event.update.message.from_user is None:
            logging.error(f"event.update.message.from_user is None\nevent is:\n{event}")
            return
    
        bot: Bot = data["bot"]
        User: baseDB.User = data["User"]
        user_id = str(event.update.message.from_user.id)
        time = timeSeconds()

        my_storage = data.get("storage")
        assert isinstance(my_storage, BaseStorage)

        chat_id = event.update.message.chat.id
        user_id = str(event.update.message.from_user.id)

        key = StorageKey(bot_id=bot.id, chat_id=chat_id, user_id=int(user_id))
        user_storage: Dict[str, List[float | bool]] = await my_storage.get_data(key)

        data["user_id"] = user_id
        data["user_lang"] = User._get(user_id)['language'] if User.is_exist(user_id) else 'en'

        if not user_storage or not user_storage.get("exception_data"):
            user_storage["exception_data"] = [time, False]
        elif user_storage["exception_data"][1]:
            return
        elif user_storage["exception_data"][0] + const.DELAY > time: # new message sent less than in DELAY sec
            user_storage["exception_data"] = [time, True]
            await my_storage.set_data(key, user_storage)
            await event.update.message.answer("Spam catched. Complete captha to continue", reply_markup=captcha_inline())
            return
        else:
            user_storage["exception_data"][0] = time
        
        await my_storage.set_data(key, user_storage)
        
        return await handler(event, data)
        
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: ErrorEvent, data: Dict[str, Any]) -> Coroutine[Any, Any, Any] | None:
        try:
            return await self.call(handler, event, data)
        except Exception as e:
            logging.error("Error middleware exception")
            raise e