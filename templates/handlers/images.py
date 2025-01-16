from typing import Type
from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import StartFSM, ManagingFSM
from templates.markups import managing_button_2, start_button, pack_link_button, single_button
from templates.funcs import is_emoji, get_create_add_info, pack_exists
from templates.media import create_InputFile
from templates.const import WATERMARK
from templates.types import Answers, texts, texts_buttons

router = Router()

@router.message(F.photo)
async def collecting_emoji_add( \
        message: types.Message,\
        state: FSMContext, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> None:
    
    message.photo
        
    answers = Answers(user_lang).get_cancel_btn()
    assert message.text