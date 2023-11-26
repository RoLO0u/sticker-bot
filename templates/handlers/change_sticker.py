from typing import Any, Type

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext

from templates.FSM_groups import ChangeStickerFSM, StartFSM
from templates.markups import start_button, single_button
from templates.types import Answers, texts, texts_buttons
from templates.const import WATERMARK
from templates.database import baseDB
from templates.funcs import is_emoji

router = Router()

@router.message(ChangeStickerFSM.change_sticker_emoji, F.sticker)
async def choosing_sticker( \
        message: types.Message, \
        state: FSMContext, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> Any:
    
    user = User(user_id)
    pack_name = user.get_additional_info()["name"]
    assert (message.sticker is not None) and (pack_name is not None)
    
    if message.sticker.set_name != pack_name+WATERMARK:
        await message.answer(texts["managing_emoji_e1"][user_lang])
        return
    
    user.change("additional_info.sticker", message.sticker.file_id)

    await state.set_state(ChangeStickerFSM.get_emoji_to_change)
    await message.answer(texts["managing_emoji_2"][user_lang].format(message.sticker.emoji))
    
@router.message(ChangeStickerFSM.change_sticker_emoji, F.text)
async def choosing_sticker_t( \
        message: types.Message, \
        state: FSMContext, \
        user_lang: str,
        ) -> Any:    
    answers = Answers(user_lang).get_cancel_btn()

    match message.text:
        case answers.cancel_btn:
            await state.set_state(StartFSM.start)
            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))
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
        ) -> Any:
    assert message.text is not None
    answers = Answers(user_lang).get_cancel_btn()
    
    match message.text:
        case answers.cancel_btn:
            await state.set_state(StartFSM.start)
            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))
        case _ if is_emoji(message.text):
            await state.set_state(StartFSM.start)
            sticker_id = User(user_id).get_additional_info()["sticker"]
            assert sticker_id is not None
            await bot.set_sticker_emoji_list(sticker_id, list(message.text))
            await message.answer(texts["managed_emoji"][user_lang], \
                reply_markup=start_button(texts_buttons["start"][user_lang], texts_buttons["change_lang"]))
        case _:
            await message.answer(texts["emoji_only_e"][user_lang])