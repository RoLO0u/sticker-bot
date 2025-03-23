from typing import Type

from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.const import COMMON_EMOJI
from templates.markups import single_button, packs_inline, start_button
from templates.types import Answers, texts, texts_buttons
from templates.FSM_groups import ManagingFSM, StartFSM
from templates.funcs import parse_emoji
from templates.handlers.add_sticker import add_sticker

router = Router()

@router.message(F.photo | F.sticker, F.chat.type=="private")
async def getting_image( \
        message: types.Message, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User], \
        state: FSMContext, \
        ) -> None:
    user = User(user_id)
    file_id: str = user["image"]
    if file_id is None:
        file_id = ""
    if message.photo:
        # Gets the highest resolution photo
        file_id = message.photo[-1].file_id
        await message.answer(texts["managing0"][user_lang],
            reply_markup=single_button(texts_buttons["cancel"][user_lang][0]))
        await message.answer_photo(file_id,
            caption=texts["choose_emoji"][user_lang],
            reply_markup=COMMON_EMOJI.markup)
    elif message.sticker:
        file_id = message.sticker.file_id
        await message.answer(texts["choose_emoji"][user_lang],
            reply_markup=single_button(texts_buttons["cancel"][user_lang][0]))
        await message.answer_sticker(file_id, reply_markup=COMMON_EMOJI.markup)
    user["image"] = file_id
    await state.set_state(ManagingFSM.emoji_inline)

@router.callback_query(ManagingFSM.emoji_inline, F.data.startswith("emo"), F.chat.type=="private")
async def choosing_emoji_query( \
        callback_query: types.CallbackQuery, \
        user_id: str, \
        user_lang: str, \
        User: type[baseDB.User], \
        state: FSMContext, \
        ) -> None:

    assert callback_query.data and isinstance(callback_query.message, types.Message)

    emoji = callback_query.data[3:]
    user = User(user_id)
    user["emoji"] = emoji

    await state.set_state(ManagingFSM.add_inline)
    await callback_query.message.edit_caption(caption=texts["choose_pack"][user_lang],
        reply_markup=packs_inline(list(user.get_packs()), texts_buttons["start"][user_lang][1]))

@router.message(ManagingFSM.emoji_inline, F.text, F.chat.type=="private")
async def choosing_emoji( \
        message: types.Message, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User], \
        state: FSMContext
        ) -> None:
    
    assert message.text

    answers = Answers(user_lang).get_cancel_btn()
    if message.text == answers.cancel_btn:
        await state.set_state(StartFSM.start)
        await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
            reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))        
        return

    emoji = parse_emoji(message.text)
    if not emoji:
        await message.answer(texts["emoji_only_e"][user_lang])
        return
    user = User(user_id)
    user["emoji"] = "".join(emoji)

    await state.set_state(ManagingFSM.add_inline)
    await message.answer(texts["choose_pack"][user_lang],
        reply_markup=packs_inline(list(user.get_packs()), texts_buttons["start"][user_lang][1]))

@router.callback_query(ManagingFSM.add_inline, F.data, F.chat.type=="private")
async def choosing_pack_query( \
        callback_query: types.CallbackQuery, \
        user_id: str, \
        User: type[baseDB.User], \
        Pack: type[baseDB.Pack], \
        state: FSMContext, \
        bot: Bot, \
        ) -> None:
    
    assert callback_query.data

    user = User(user_id)

    pack = Pack(callback_query.data)
    if not all([pack, pack.includes(user.id)]):
        return

    user["name"] = callback_query.data

    assert isinstance(callback_query.message, types.Message)
    
    await add_sticker(user, bot, callback_query.message, state)

@router.message(ManagingFSM.add_inline, F.chat.type=="private")
async def choosing_pack( \
        message: types.Message, \
        user_lang: str, \
        state: FSMContext
        ) -> None:
    
    assert message.text

    answers = Answers(user_lang).get_cancel_btn()
    if message.text == answers.cancel_btn:
        await state.set_state(StartFSM.start)
        await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
            reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))        
        return