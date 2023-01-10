import logging

from typing import Dict, Any, Union

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates import database
from templates.FSM_groups import CreatingFSM, StartFSM
from templates.markups import start_button, pack_link_button, single_button
from templates.funcs import random_string, is_emoji, get_create_add_info
from templates.const import WATERMARK

router = Router()


@router.message(CreatingFSM.creating_name, F.text)
async def creating_name(                                \
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

            await state.set_state(StartFSM.start)

            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

        case _ if len(message.text) <= 64:

            name = random_string()

            while name in database.get_packs_name():
                name = random_string()
            
            database.create_pack(user_id, name, message.text)
            database.change_title(user_id, message.text)
            await state.set_state(CreatingFSM.collecting_emoji)
            database.change_name(user_id, name)

            await message.answer(texts["creating2"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))

        case _:
            await message.answer(texts["creating1_e1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))


@router.message(CreatingFSM.collecting_emoji, F.text)
async def collecting_emoji(                             \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        user_id: str,                                   \
        user_lang: str                                  \
        ) -> Any:

    class Answers:
        create_btn = texts["cancel_button"][user_lang]

    match message.text:

        case Answers.create_btn:

            await state.set_state(StartFSM.start)
            database.delete_pack(user_id)
            database.change_name(user_id, None)

            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
        
        case _:

            if is_emoji(message.text):

                database.change_emoji(user_id, message.text)
                await state.set_state(CreatingFSM.collecting_photo)

                await message.answer(texts["creating3"][user_lang], \
                    reply_markup=single_button(texts["cancel_button"][user_lang]))

            else:
                await message.answer(texts["emoji_only_e"][user_lang], \
                    reply_markup=single_button(texts["cancel_button"][user_lang]))


@router.message(CreatingFSM.collecting_photo, F.text)
async def collecting_photo_t(                           \
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

            await state.set_state(StartFSM.start)
            additional_info = database.get_additional_info(user_id)
            database.delete_pack(user_id, additional_info["name"])
            database.change_emoji(user_id, None)
            database.change_name(user_id, None)

            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
        
        case _:
            await message.answer(texts["image_only_e"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))


@router.message(CreatingFSM.collecting_photo, F.photo)
async def collecting_photo(                             \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        bot: Bot,                                       \
        user_id: str,                                   \
        user_lang: str                                  \
        ) -> Any:

    # TODO: make multiple emojis to sticker possible
    # TODO: make webm and tgs image format possible

    pack_name, pack_name_plus, title, photo, emoji = \
        await get_create_add_info(user_id, bot.get_file, message.photo, bot.download_file)
    
    print(pack_name_plus)
    
    try:
        if await bot.create_new_sticker_set(user_id=int(user_id), name=pack_name_plus, \
            title=title, emojis=emoji, png_sticker=photo):

            await state.set_state(StartFSM.start)
            database.change_name(user_id, None)
            database.change_emoji(user_id, None)
            database.change_title(user_id, None)
            database.change_pack_status(pack_name, "maked")

            await message.answer(texts["created1"][user_lang], \
                reply_markup=pack_link_button(texts["created_inline"][user_lang], "https://t.me/addstickers/" + pack_name + WATERMARK))
            await message.answer(texts["created2"][user_lang], \
                reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))

        else:
            await message.answer(texts["unknown_exception_1"][user_lang]+'2')

    # TODO explore what exception happens when telegram don't want to user create pack

    except Exception as e:
        await message.answer(texts["known_e_1"][user_lang]+str(e).split()[-1])

        # temporary
        await message.answer(f"""Please send this message to @feddunn\n{type(e).__name__}""")
        
        logging.critical(e)