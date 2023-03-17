from typing import Dict, Any, Union

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates import database
from templates.FSM_groups import StartFSM, ManagingFSM
from templates.markups import managing_button_2, start_button, pack_link_button, single_button
from templates.funcs import is_emoji, get_create_add_info, pack_exists
from templates.const import WATERMARK

router = Router()

@router.message(ManagingFSM.collecting_emoji_add, F.text)
async def collecting_emoji_add(                         \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        user_id: str,                                   \
        user_lang: str                                  \
        ) -> Any:
    
    class Answers:
        cancel_btn = texts["cancel_button"][user_lang]

    match message.text:

        case Answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))

        case _:

            if is_emoji(message.text):

                await state.set_state(ManagingFSM.collecting_photo_add)
                database.change_emoji(user_id, message.text)
                await message.answer(texts["managing_add_2"][user_lang], \
                    reply_markup=single_button(texts["cancel_button"][user_lang]))
        
            else:
                await message.answer(texts["emoji_only_e"][user_lang])

@router.message(ManagingFSM.collecting_photo_add, F.text)
async def collecting_photo_add_t(                       \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        user_id: str,                                   \
        user_lang: str                                  \
        ) -> Any:
    
    class Answers:
        cancel_btn = texts["cancel_button"][user_lang]

    match message.text:

        case Answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            database.change_emoji(user_id, None)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))

        case _:
            await message.answer(texts["image_only_e"][user_lang])

@router.message(ManagingFSM.collecting_photo_add, F.photo)
async def collecting_photo_add(                         \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        bot: Bot,                                       \
        user_id: str,                                   \
        user_lang: str                                  \
        ) -> Any:

    pack_name, pack_name_plus, _, photo, emoji = \
        await get_create_add_info(user_id, bot.get_file, message.photo, bot.download_file)

    if not await pack_exists(bot.get_sticker_set, pack_name_plus):
        state.set_state(StartFSM.start)
        database.delete_pack(user_id, pack_name)
        database.change_name(user_id, None)
        database.change_emoji(user_id, None)
        await message.answer(texts["managing_add_e"][user_lang], \
            reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))
        return

    try:

        if await bot.add_sticker_to_set(int(user_id), pack_name_plus, \
                emoji, png_sticker=photo):
            
            await state.set_state(StartFSM.start)
            database.change_name(user_id, None)
            database.change_emoji(user_id, None)
            
            await message.answer(texts["added1"][user_lang], \
                reply_markup=pack_link_button(texts["created_inline"][user_lang], "https://t.me/addstickers/" + pack_name + WATERMARK))
            await message.answer(texts["created2"][user_lang], \
                reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))

    except Exception as e:

        await message.answer(texts["known_e_1"][user_lang]+str(e).split()[-1])

        # temporary
        await message.answer(f"""Please send this message to @feddunn\n{type(e).__name__}""")
        
        raise e