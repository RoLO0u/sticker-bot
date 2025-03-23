from typing import Type
from aiogram import Router, F, types

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import StartFSM, JoiningFSM, ManagingFSM
from templates.markups import start_button, managing_button_2
from templates.types import Answers, texts, texts_buttons

router = Router()

@router.message()
async def group_start( \
        message: types.Message, \
        state: FSMContext, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> None:
    
    await message.answer("Hello")