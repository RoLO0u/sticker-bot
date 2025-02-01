from typing import Type

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import CreatingFSM, StartFSM
from templates.markups import start_button, pack_link_button, single_button, create_options
from templates.funcs import random_string, is_emojis, get_create_add_info
from templates.media import create_input_file
from templates.const import WATERMARK
from templates.types import Answers, texts, texts_buttons

router = Router()

@router.callback_query(F.data == "crp")
async def creating_pack_inline( \
        callback_query: types.CallbackQuery, \
        state: FSMContext, \
        user_lang: str, \
        ) -> None:
    assert isinstance(callback_query.message, types.Message)
    await state.set_state(CreatingFSM.choosing_option)
    await callback_query.message.answer(texts["start_opts"][user_lang], \
        reply_markup=create_options(texts_buttons["start_opts"][user_lang]))

@router.message(CreatingFSM.choosing_option, F.text)
async def choosing_option( \
        message: types.Message, \
        state: FSMContext, \
        user_lang: str, \
        ) -> None:
    
    answers = Answers(user_lang).get_start_opts_btns()

    text = message.text
    assert text

    match text:
        case answers.from_scratch:
            await state.set_state(CreatingFSM.creating_name)
            await message.answer(texts["creating1"][user_lang], parse_mode="HTML", \
                reply_markup=single_button(texts["cancel_button"][user_lang]))
        case answers.cancel_btn:
            await state.set_state(StartFSM.start)
            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))
        case answers.copy:
            await state.set_state(CreatingFSM.copying_pack)
            await message.answer(texts["copying_pack"][user_lang], parse_mode="HTML",
                reply_markup=single_button(texts["cancel_button"][user_lang]))

@router.message(CreatingFSM.creating_name, F.text)
async def creating_name( \
        message: types.Message, \
        state: FSMContext, \
        user_id: str, \
        user_lang: str, \
        MiscDB: Type[baseDB.MiscDB], \
        bot: Bot, \
        User: Type[baseDB.User], \
        Pack: Type[baseDB.Pack] \
        ) -> None:

    answers = Answers(user_lang).get_cancel_btn()
    
    text = message.text
    assert text # text will never be none because router has filter

    match text:

        case answers.cancel_btn:
            await state.set_state(StartFSM.start)
            User(user_id).change("stickers", [])
            User(user_id).change("emojis", [])
            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))

        case _ if len(text) <= 64:

            name = random_string()
            while name in MiscDB.get_packs_name():
                name = random_string()

            user = User(user_id)
            User(user_id).create(name, text)
            user.change_title(text)
            user.change_name(name)

            # If user chose from scratch
            if not user["stickers"]:
                await state.set_state(CreatingFSM.collecting_emoji)
                await message.answer(texts["creating2"][user_lang], \
                    reply_markup=single_button(texts["cancel_button"][user_lang]))
                return
            
            pack_name, pack_name_plus, title, _ = \
                await get_create_add_info(user_id, User)
            assert title

            stickers = []
            ran = len(user["stickers"])
            too_much = ran > 50
            ran = 50 if too_much else ran
            for i in range(ran):
                stickers.append(types.InputSticker(sticker=user["stickers"][i], format="static", emoji_list=is_emojis(user["emojis"][i]))) #list(user["emojis"][i])

            try:
                if await bot.create_new_sticker_set(user_id=int(user_id), name=pack_name_plus, \
                    title=title, stickers=stickers, sticker_format="static"):

                    if too_much:
                        ran = len(user["stickers"])
                        for i in range(50, ran):
                            await bot.add_sticker_to_set(int(user_id), pack_name_plus, \
                                sticker=types.InputSticker(sticker=user["stickers"][i], format="static", emoji_list=[user["emojis"][i]]))

                    await state.set_state(StartFSM.start)
                    user = User(user_id)
                    user.change_name(None)
                    user.change_emoji(None)
                    user.change_title(None)
                    user.change("stickers", [])
                    user.change("emojis", [])
                    Pack(pack_name).change_status("maked") # TODO migrate 'maked' to 'made' (cringe)

                    await message.answer(texts["created1"][user_lang], \
                        reply_markup=pack_link_button(texts["created_inline"][user_lang], "https://t.me/addstickers/" + pack_name + str(WATERMARK)))
                    await message.answer(texts["created2"][user_lang], \
                        reply_markup=start_button(texts_buttons["start"][user_lang], texts_buttons["change_lang"]))

                else:
                    await message.answer(texts["unknown_exception_1"][user_lang]+'2')

            # TODO explore what exception happens when telegram doesn't want to user create pack

            except Exception as e:
                await message.answer(texts["known_e_1"][user_lang]+str(e).split()[-1])

                # temporary
                await message.answer(f"""Please send this message to @feddunn\n{type(e).__name__}""")

                raise e

        case _:
            await message.answer(texts["naming_e1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))


@router.message(CreatingFSM.collecting_emoji, F.text)
async def collecting_emoji( \
        message: types.Message, \
        state: FSMContext, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> None:

    answers = Answers(user_lang).get_cancel_btn()

    match message.text:

        case answers.cancel_btn:

            await state.set_state(StartFSM.start)
            user = User(user_id)
            user.delete_pack()
            user.change_name(None)

            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))

        case _:

            if is_emojis(message.text): # type: ignore

                User(user_id).change_emoji(message.text)
                await state.set_state(CreatingFSM.collecting_photo)

                await message.answer(texts["creating3"][user_lang], \
                    reply_markup=single_button(texts["cancel_button"][user_lang]))

            else:
                await message.answer(texts["emoji_only_e"][user_lang], \
                    reply_markup=single_button(texts["cancel_button"][user_lang]))


@router.message(CreatingFSM.collecting_photo, F.text)
async def collecting_photo_t( \
        message: types.Message, \
        state: FSMContext, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> None:

    answers = Answers(user_lang).get_cancel_btn()

    match message.text:

        case answers.cancel_btn:

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


@router.message(CreatingFSM.collecting_photo, F.photo | F.sticker)
async def collecting_photo( \
        message: types.Message, \
        state: FSMContext, \
        bot: Bot, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User], \
        Pack: Type[baseDB.Pack] \
        ) -> None:

    # TODO: make webm and tgs image format possible

    if message.sticker:
        file = message.sticker.file_id
    elif message.photo:
        file = await create_input_file(bot, message.photo)

    pack_name, pack_name_plus, title, emoji = \
        await get_create_add_info(user_id, User)
    assert title
    assert emoji

    try:
        if await bot.create_new_sticker_set(user_id=int(user_id), name=pack_name_plus, \
            title=title, stickers=[types.InputSticker(sticker=file, format="static", emoji_list=is_emojis(emoji))], sticker_format="static"):

            await state.set_state(StartFSM.start)
            user = User(user_id)
            user.change_name(None)
            user.change_emoji(None)
            user.change_title(None)
            Pack(pack_name).change_status("maked") # TODO migrate 'maked' to 'made' (cringe)

            await message.answer(texts["created1"][user_lang], \
                reply_markup=pack_link_button(texts["created_inline"][user_lang], "https://t.me/addstickers/" + pack_name + str(WATERMARK)))
            await message.answer(texts["created2"][user_lang], \
                reply_markup=start_button(texts_buttons["start"][user_lang], texts_buttons["change_lang"]))

        else:
            await message.answer(texts["unknown_exception_1"][user_lang]+'2')

    # TODO explore what exception happens when telegram doesn't want to user create pack

    except Exception as e:
        await message.answer(texts["known_e_1"][user_lang]+str(e).split()[-1])

        # temporary
        await message.answer(f"""Please send this message to @feddunn\n{type(e).__name__}""")

        raise e
    
@router.message(CreatingFSM.copying_pack, F.text)
async def copying_pack_t( \
        message: types.Message, \
        state: FSMContext, \
        user_lang: str, \
        ) -> None:

    answers = Answers(user_lang).get_cancel_btn()
    match message.text:
        case answers.cancel_btn:
            await state.set_state(StartFSM.start)
            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))
        case _:
            await message.answer(texts["sticker_only_e"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))
            
@router.message(CreatingFSM.copying_pack, F.sticker)
async def copying_pack( \
        message: types.Message, \
        state: FSMContext, \
        bot: Bot, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User], \
        ) -> None:
    
    assert message.sticker

    if not message.sticker.set_name:
        await message.answer(texts["sticker_only_e"][user_lang], \
            reply_markup=single_button(texts["cancel_button"][user_lang]))
        return
    
    sticker_set = await bot.get_sticker_set(message.sticker.set_name)

    if sticker_set.sticker_type != "regular":
        await message.answer(texts["sticker_only_e"][user_lang], \
            reply_markup=single_button(texts["cancel_button"][user_lang]))
        return
    
    await state.set_state(CreatingFSM.creating_name)
    
    user = User(user_id)
    user.change("stickers", [sticker.file_id for sticker in sticker_set.stickers])
    user.change("emojis", [sticker.emoji for sticker in sticker_set.stickers])

    await message.answer(texts["creating1"][user_lang], parse_mode="HTML", \
        reply_markup=single_button(texts["cancel_button"][user_lang]))