from aiohttp import web
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from templates import const

async def set_webhook(bot: Bot) -> None:
    bot_info = await bot.me()
    assert bot_info.username
    const.WATERMARK._update(bot_info.username)
    assert const.WEBHOOK_SSL_CERT
    await bot.set_webhook(
        f"{const.BASE_WEBHOOK_URL}{const.WEBHOOK_PATH}",
        secret_token=const.WEBHOOK_SECRET,
    )

async def run_polling(dp: Dispatcher, bot: Bot):
    bot_info = await bot.me()
    assert bot_info.username
    const.WATERMARK._update(bot_info.username)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

def on_launch(bot: Bot, dp: Dispatcher) -> None:

    if const.WEBHOOK == "False":
        asyncio.run(run_polling(dp, bot))
    elif const.WEBHOOK == "True":
        dp.startup.register(set_webhook)

        app = web.Application()
        webhook_request_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=const.WEBHOOK_SECRET
        )
        webhook_request_handler.register(app, path=const.WEBHOOK_PATH)

        setup_application(app, dp, bot=bot)

        web.run_app(app, host=const.WEB_SERVER_HOST, port=const.WEB_SERVER_PORT)