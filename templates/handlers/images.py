from typing import Type
from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import ImagesFSM
from templates.const import COMMON_EMOJI
from templates.markups import single_button
from templates.types import Answers, texts, texts_buttons

router = Router()

@router.message(F.photo)
async def getting_image( \
        message: types.Message, \
        state: FSMContext, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User], \
        ) -> None:
    
    assert message.photo

    await message.answer(texts["managing0"][user_lang],
            reply_markup=single_button(texts_buttons["cancel"][user_lang][0]))
    # Telegram returns two version of photo for each photo: smaller and bigger ones
    # TODO:
    # Telegram uses different amount of duplicates depending on the file_size
    # 90 (or maybe 160), 320, 620, 1280
    photos = [photo.file_id for photo in message.photo[::2]]
    User(user_id).change("images", photos)


    print(photos, message.photo, sep="\n")

    if len(photos) == 1:
        await state.set_state(ImagesFSM.choosing_emoji)
        await message.answer(texts["choose_emoji"][user_lang],
            reply_markup=COMMON_EMOJI.markup)
    
# @router.message(ImagesFSM.choosing_emoji, F.text)
# async def getting_emoji_t( \
#         message: types.Message, \
#         state: FSMContext, \ 
#         )