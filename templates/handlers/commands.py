from typing import Type

from aiogram import types, Router, Bot, F
from aiogram.filters import Command
from aiogram.utils.markdown import hide_link
from aiogram.fsm.context import FSMContext

from templates import markups, const
from templates.database import baseDB
from templates.FSM_groups import StartFSM
from templates.types import texts, texts_buttons

router = Router()

@router.message(Command("start"), F.chat.type=="private")
async def start( \
        message: types.Message, \
        state: FSMContext, \
        user: baseDB.User \
        ) -> None:
    
    await state.set_state(StartFSM.start)

    user.change("stickers", [])
    user.change("emojis", [])

    await message.answer(texts["start"][user.lang], parse_mode="HTML", \
        reply_markup=markups.start_button( texts_buttons["start"][user.lang], texts_buttons["change_lang"] ))
    
@router.message(Command("help"), F.chat.type=="private")
async def help( \
        message: types.Message, \
        bot: Bot, \
        user: baseDB.User \
        ) -> None:

    bot_info = await bot.me()
    assert bot_info.username
    const.WATERMARK._update(bot_info.username)

    await message.answer(f"{hide_link('https://i.imgur.com/ZRv0bDC.png')}"
        f"{texts['help_1'][user.lang]}", parse_mode="HTML")