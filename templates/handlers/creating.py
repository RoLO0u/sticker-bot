from typing import Any, Type

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import CreatingFSM, StartFSM
from templates.markups import start_button, pack_link_button, single_button
from templates.funcs import random_string, is_emoji, get_create_add_info
from templates.const import WATERMARK
from templates.types import Texts, TextsButtons

router = Router()


@router.message(CreatingFSM.creating_name, F.text)
async def creating_name(                                \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        user_id: str,                                   \
        user_lang: str,                                 \
        MiscDB: Type[baseDB.MiscDB],                    \
        User: Type[baseDB.User]                         \
        ) -> Any:

    class Answers:
        cancel_btn = texts_buttons["cancel"][user_lang][0]
        
    text = message.text
    assert text is not None # text will never be none because router has filter

    match text:

        case Answers.cancel_btn:

            await state.set_state(StartFSM.start)

            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))

        case _ if len(text) <= 64:

            name = random_string()
            while name in MiscDB.get_packs_name():
                name = random_string()
            
            user = User(user_id)
            User(user_id).create(name, text)
            user.change_title(text)
            await state.set_state(CreatingFSM.collecting_emoji)
            user.change_name(name)

            await message.answer(texts["creating2"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))

        case _:
            await message.answer(texts["creating1_e1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))


@router.message(CreatingFSM.collecting_emoji, F.text)
async def collecting_emoji(                             \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        user_id: str,                                   \
        user_lang: str,                                 \
        User: Type[baseDB.User]                         \
        ) -> Any:

    class Answers:
        create_btn = texts_buttons["cancel"][user_lang][0]

    match message.text:

        case Answers.create_btn:

            await state.set_state(StartFSM.start)
            user = User(user_id)
            user.delete_pack()
            user.change_name(None)

            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))
        
        case _:

            if is_emoji(message.text): # type: ignore

                User(user_id).change_emoji(message.text)
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
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        user_id: str,                                   \
        user_lang: str,                                 \
        User: Type[baseDB.User]                         \
        ) -> Any:

    class Answers:
        cancel_btn = texts_buttons["cancel"][user_lang][0]

    match message.text:

        case Answers.cancel_btn:

            await state.set_state(StartFSM.start)
            user = User(user_id)
            user.delete_pack()
            user.change_emoji(None)
            user.change_name(None)

            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))
        
        case _:
            await message.answer(texts["image_only_e"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))


@router.message(CreatingFSM.collecting_photo, F.photo)
async def collecting_photo(                             \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        bot: Bot,                                       \
        user_id: str,                                   \
        user_lang: str,                                 \
        User: Type[baseDB.User],                        \
        Pack: Type[baseDB.Pack]                         \
        ) -> Any:

    # TODO: make multiple emojis to sticker possible
    # TODO: make webm and tgs image format possible

    pack_name, pack_name_plus, title, photo, emoji = \
        await get_create_add_info(user_id, User, bot.get_file, message.photo, bot.download_file)
    assert title is not None
    assert emoji is not None
    
    try:
        if await bot.create_new_sticker_set(user_id=int(user_id), name=pack_name_plus, \
            title=title, emojis=emoji, png_sticker=photo):

            await state.set_state(StartFSM.start)
            user = User(user_id)
            user.change_name(None)
            user.change_emoji(None)
            user.change_title(None)
            Pack(pack_name).change_status("maked") # TODO migrate 'maked' to 'made' (cringe)

            await message.answer(texts["created1"][user_lang], \
                reply_markup=pack_link_button(texts["created_inline"][user_lang], "https://t.me/addstickers/" + pack_name + WATERMARK))
            await message.answer(texts["created2"][user_lang], \
                reply_markup=start_button(texts_buttons["start"][user_lang], texts_buttons["change_lang"]))

        else:
            await message.answer(texts["unknown_exception_1"][user_lang]+'2')

    # TODO explore what exception happens when telegram doesn't want to user create pack
    # TODO maybe create something to save logs

    except Exception as e:
        await message.answer(texts["known_e_1"][user_lang]+str(e).split()[-1])

        # temporary
        await message.answer(f"""Please send this message to @feddunn\n{type(e).__name__}""")
        
        raise e