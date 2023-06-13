from typing import Any

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.utils.markdown import hide_link
from aiogram.fsm.context import FSMContext

from templates import markups
from templates.FSM_groups import StartFSM
from templates.types import Texts, TextsButtons

router = Router()

@router.message(Command("start"))
async def start(                                \
        message: types.Message,                 \
        state: FSMContext,                      \
        texts: Texts,                           \
        texts_buttons: TextsButtons,            \
        user_lang: str                          \
        ) -> Any:
    
    await state.set_state(StartFSM.start)

    await message.answer(texts["start"][user_lang], parse_mode="HTML", \
        reply_markup=markups.start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))
    
@router.message(Command("help"))
async def help(                                        \
        message: types.Message,                        \
        texts: Texts,                                  \
        user_lang: str                                 \
        ) -> Any:

    await message.answer(f"{hide_link('https://i.imgur.com/ZRv0bDC.png')}"
        f"{texts['help_1'][user_lang]}", parse_mode="HTML")