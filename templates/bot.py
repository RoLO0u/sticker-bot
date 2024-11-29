import os

from aiogram import Bot, Dispatcher, F

from templates import Exceptions, throttling, const
from templates.handlers import \
    add_sticker, change_sticker, commands, creating, \
    delete, group, inline, managing, start, errors
from templates.types import texts, texts_buttons

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

async def run() -> None:

    # configuring aiogram bot

    TOKEN = os.getenv("BOT_TOKEN")

    if TOKEN == None:
        raise Exceptions.TokenIsNotDefined()

    bot = Bot(TOKEN)

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
    dp["bot_info"] = await bot.me()

    const.WATERMARK._update(dp["bot_info"].username)
        
    # Filters and middlewares only work for text messages
    # Setting up middleware for every message type:
    # inline, photo, sticker, etc. breaks middleware
    # because text message provides Message event type
    # but Sticker provides Update event type
    # https://docs.aiogram.dev/en/latest/dispatcher/middlewares.html
    dp.message.filter(F.chat.type=="private")
    dp.message.middleware(throttling.AntiFloodMiddleware())
    
    for handler in add_sticker, change_sticker, commands, creating, \
            delete, group, inline, managing, start, errors:
        
        dp.include_router(handler.router)
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()