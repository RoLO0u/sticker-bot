import logging
import json
import os

from aiogram import Bot, Dispatcher, F

# from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from templates import Exceptions, throttling
from templates.handlers import *
from templates.mongo import MongoStorage

async def run():

    # configuring storage
    
    URI = os.getenv("MONGO_URL")

    storage = MongoStorage(uri=URI)

    # TODO move not bot work to other files
    # configuring aiogram bot

    logging.basicConfig(level=logging.INFO)

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

    dp.message.filter(F.chat.type=="private")

    dp.include_router(commands.router)
    dp.include_router(start.router)
    dp.include_router(managing.router)
    dp.include_router(creating.router)
    dp.include_router(inline.router)
    dp.include_router(add_sticker.router)
    dp.include_router(delete.router)
    dp.include_router(group.router)

    dp.message.middleware(throttling.AntiFloodMiddleware())

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

    # TODO correction of state
                
    # TODO FUTURE delete set from his members also