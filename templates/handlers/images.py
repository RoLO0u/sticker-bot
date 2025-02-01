from typing import Type
from aiogram import types, Router, F

from templates.database import baseDB
from templates.const import COMMON_EMOJI
from templates.markups import single_button, packs_inline
from templates.types import texts, texts_buttons

router = Router()

@router.message(F.photo)
async def getting_image( \
        message: types.Message, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User], \
        ) -> None:
    assert message.photo
    # Gets the highest resolution photo
    await message.answer(texts["managing0"][user_lang],
        reply_markup=single_button(texts_buttons["cancel"][user_lang][0]))
    photo = message.photo[-1]
    user = User(user_id)

    images: list[str] = user["images"]
    images.append(photo.file_id)

    user.change("images", images)

    await message.answer_photo(photo.file_id,
        caption=texts["choose_emoji"][user_lang],
        reply_markup=COMMON_EMOJI.markup)

@router.callback_query(F.data.startswith("emo"))
async def choosing_emoji_query(
        callback_query: types.CallbackQuery,
        user_id: str,
        user_lang: str,
        User: type[baseDB.User]
        ) -> None:

    assert callback_query.data and isinstance(callback_query.message, types.Message)

    emoji = callback_query.data[-1]
    user = User(user_id)

    user.change_emoji(emoji)

    await callback_query.message.edit_caption(caption=texts["choose_pack"][user_lang],
        reply_markup=packs_inline([{'1': '1'}], 's'))