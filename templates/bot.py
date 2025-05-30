import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from templates import Exceptions, throttling
from templates.handlers import routers
from templates.types import texts, texts_buttons
from templates.launch import on_launch

def get_db():
    
    db_type = os.getenv("DB")
    
    if db_type == "mongodb":
        from templates.database.fsm.mongo import MongoStorage
        from templates.database import mongodb
        URI = os.getenv("MONGO_URI")
        return mongodb, MongoStorage(uri=URI)
        
    elif db_type == "postgresql":
        from templates.database.fsm.postgres import PostgreStorage
        from templates.database import postgresql
        postgresql.MiscDB.create_tables()
        return postgresql, PostgreStorage(**postgresql.kwargs) # type: ignore
        
    else:
        raise Exceptions.InvalidEnvException("DB variable is not valid (either mongodb or postgresql)")

def run() -> None:

    # configuring aiogram bot

    TOKEN = os.getenv("BOT_TOKEN")
    if TOKEN == None:
        raise Exceptions.TokenIsNotDefined()

    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # configuring storage

    mainDB, storage = get_db()
    dp = Dispatcher(storage=storage, name="main")
    
    dp["User"] = mainDB.User
    dp["Pack"] = mainDB.Pack
    dp["MiscDB"] = mainDB.MiscDB
    dp["dp"] = dp
    dp["storage"] = storage
    dp["texts"] = texts
    dp["texts_buttons"] = texts_buttons
    dp["bot"] = bot
        
    # Filters and middlewares only work for text messages
    # Setting up middleware for every message type:
    # inline, photo, sticker, etc. breaks middleware
    # because text message provides Message event type
    # but Sticker provides Update event type
    # https://docs.aiogram.dev/en/latest/dispatcher/middlewares.html
    dp.message.middleware(throttling.AntiFloodMiddleware())
    dp.callback_query.middleware(throttling.AntiFloodMiddleware())
    
    dp.include_routers(*routers)
    
    on_launch(bot, dp)