from typing import Type

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext

from templates.FSM_groups import ChangeStickerFSM, ManagingFSM
from templates.markups import single_button, managing_button_2
from templates.types import Answers, texts, texts_buttons
from templates.const import WATERMARK
from templates.database import baseDB
from templates.funcs import is_emojis

router = Router()

@router.message(ChangeStickerFSM.change_sticker_emoji, F.sticker)
async def choosing_sticker( \
        message: types.Message, \
        state: FSMContext, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> None:
    
    user = User(user_id)
    pack_name = user.user["name"]
    assert (message.sticker) and (pack_name)
    
    if message.sticker.set_name != pack_name+str(WATERMARK):
        await message.answer(texts["managing_emoji_e1"][user_lang])
        return
    
    user.change("sticker", message.sticker.file_id)

    await state.set_state(ChangeStickerFSM.get_emoji_to_change)
    await message.answer(texts["managing_emoji_2"][user_lang].format(message.sticker.emoji))
    
@router.message(ChangeStickerFSM.change_sticker_emoji, F.text)
async def choosing_sticker_t( \
        message: types.Message, \
        state: FSMContext, \
        user_lang: str,
        ) -> None:    
    answers = Answers(user_lang).get_cancel_btn()

    match message.text:
        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))
        case _:
            await message.answer(texts["sticker_only_e"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))
            
@router.message(ChangeStickerFSM.get_emoji_to_change, F.text)
async def get_emoji( \
        message: types.Message, \
        state: FSMContext, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User], \
        bot: Bot \
        ) -> None:
    assert message.text
    answers = Answers(user_lang).get_cancel_btn()
    
    match message.text:
        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))
        case _ if is_emojis(message.text):
            await state.set_state(ManagingFSM.menu)
            sticker_id = User(user_id)["sticker"]
            assert sticker_id
            await bot.set_sticker_emoji_list(sticker_id, is_emojis(message.text))
            await message.answer(texts["managed_emoji"][user_lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))
        case _:
            await message.answer(texts["emoji_only_e"][user_lang])