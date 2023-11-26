from typing import Any, Type
from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import StartFSM, ManagingFSM
from templates.markups import managing_button_2, start_button, pack_link_button, single_button
from templates.funcs import is_emoji, get_create_add_info, pack_exists
from templates.const import WATERMARK
from templates.types import Answers, texts, texts_buttons

router = Router()

@router.message(ManagingFSM.collecting_emoji_add, F.text)
async def collecting_emoji_add( \
        message: types.Message,\
        state: FSMContext, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> Any:
        
    answers = Answers(user_lang).get_cancel_btn()

    match message.text:

        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))

        case _:

            if is_emoji(message.text): # type: ignore
                                       # ignore because router has filter for text already

                await state.set_state(ManagingFSM.collecting_photo_add)
                User(user_id).change_emoji(message.text)
                await message.answer(texts["managing_add_2"][user_lang], \
                    reply_markup=single_button(texts_buttons["cancel"][user_lang][0]))
        
            else:
                await message.answer(texts["emoji_only_e"][user_lang])

@router.message(ManagingFSM.collecting_photo_add, F.text)
async def collecting_photo_add_t( \
        message: types.Message, \
        state: FSMContext, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> Any:
    
    answers = Answers(user_lang).get_cancel_btn()

    match message.text:

        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            User(user_id).change_emoji(None)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))

        case _:
            await message.answer(texts["image_only_e"][user_lang])

@router.message(ManagingFSM.collecting_photo_add, F.photo)
async def collecting_photo_add( \
        message: types.Message, \
        state: FSMContext, \
        bot: Bot, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> Any:

    pack_name, pack_name_plus, _, photo, emoji = \
        await get_create_add_info(user_id, User, bot.get_file, message.photo, bot.download_file)

    if not await pack_exists(bot.get_sticker_set, pack_name_plus):
        await state.set_state(state=StartFSM.start)
        user = User(user_id)
        user.delete_pack()
        user.change_name(None)
        user.change_emoji(None)
        await message.answer(texts["managing_add_e"][user_lang], \
            reply_markup=start_button(texts_buttons["start"][user_lang], texts_buttons["change_lang"]))
        return

    try:
        
        assert emoji

        if await bot.add_sticker_to_set(int(user_id), pack_name_plus, sticker=types.InputSticker(sticker=photo, emoji_list=list(emoji))):
            
            await state.set_state(StartFSM.start)
            user = User(user_id)
            user.change_name(None)
            user.change_emoji(None)
            
            await message.answer(texts["added1"][user_lang], \
                reply_markup=pack_link_button(texts["created_inline"][user_lang], "https://t.me/addstickers/" + pack_name + WATERMARK))
            await message.answer(texts["created2"][user_lang], \
                reply_markup=start_button(texts_buttons["start"][user_lang], texts_buttons["change_lang"]))

    except Exception as e:

        await message.answer(texts["known_e_1"][user_lang]+str(e).split()[-1])

        # temporary
        # update: maybe
        await message.answer(f"""Please send this message to @feddunn\n{type(e).__name__}""")
        
        raise e