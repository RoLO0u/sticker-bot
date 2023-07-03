import json
import logging
import os

from aiogram import Bot, Dispatcher, F

from templates import Exceptions, throttling, const
from templates.handlers import *

async def run():
    
    # configuring aiogram bot

    TOKEN = os.getenv("BOT_TOKEN")

    if TOKEN == None:
        raise Exceptions.TokenDoesNotDefined()

    with open("texts.json", "r", encoding="utf-8") as raw:
        texts = json.load(raw)
    with open("texts_buttons.json", "r", encoding="utf-8") as raw:
        texts_buttons = json.load(raw)

    bot = Bot(TOKEN)

    # configuring storage
    
    db_type = os.getenv("DB")
    
    if db_type == "mongodb":
        from templates.database.fsm.mongo import MongoStorage
        from templates.database import mongodb
        
        URI = os.getenv("MONGO_URI")
        storage = MongoStorage(uri=URI)
        mainDB = mongodb
        
    elif db_type == "postgresql":
        from templates.database.fsm.postgres import PostgreStorage
        from templates.database import postgresql
        postgresql.MiscDB.create_tables()
        storage = PostgreStorage(**postgresql.kwargs) # type: ignore
        mainDB = postgresql
        
    else:
        raise Exceptions.InvalidEnvException("DB variable is not valid (either mongodb or postgresql)")

    dp = Dispatcher(storage=storage, name="main")
    
    dp["User"] = mainDB.User
    dp["Pack"] = mainDB.Pack
    dp["MiscDB"] = mainDB.MiscDB
    dp["dp"] = dp
    dp["storage"] = storage
    dp["texts"] = texts
    dp["texts_buttons"] = texts_buttons
    dp["bot"] = bot
    dp["bot_info"] = await bot.me()
        
    if dp["bot_info"].username == const.WATERMARK[4:]:
        logging.info("Bot name and token are valid")
    else:
        raise Exceptions.InvalidEnvException

    dp.message.filter(F.chat.type=="private")

    for handler in (commands, start, managing, creating, inline, add_sticker, delete, group, errors):
        dp.include_router(handler.router)

    dp.message.middleware(throttling.AntiFloodMiddleware())

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()