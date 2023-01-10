import json
import logging
import os

from aiogram import Bot, Dispatcher, F

# from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from templates import Exceptions, throttling, const
from templates.handlers import *
from templates.mongo import MongoStorage

async def run():

    # configuring storage
    
    URI = os.getenv("MONGO_URI")

    storage = MongoStorage(uri=URI)
    
    # configuring aiogram bot

    TOKEN = os.getenv("BOT_TOKEN")

    if TOKEN == None:
        raise Exceptions.TokenDoesNotDefined()

    with open("texts.json", "r", encoding="utf-8") as raw_texts:
        texts = json.load(raw_texts)

    bot = Bot(TOKEN)

    dp = Dispatcher(storage=storage, name="main")

    dp["dp"] = dp
    dp["storage"] = storage
    dp["texts"] = texts
    dp["bot"] = bot
    dp["bot_info"] = await bot.me()
        
    if dp["bot_info"].username == const.WATERMARK[4:]:
        logging.info("Bot name and token are valid")
    else:
        raise Exceptions.InvalidEnvException

    dp.message.filter(F.chat.type=="private")

    for handler in (commands, start, managing, creating, inline, add_sticker, delete, group):
        dp.include_router(handler.router)

    dp.message.middleware(throttling.AntiFloodMiddleware())

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
                
    # TODO FUTURE delete set from his members also