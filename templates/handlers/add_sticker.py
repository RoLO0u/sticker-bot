from typing import Type
from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import StartFSM, ManagingFSM
from templates.markups import managing_button_2, start_button, pack_link_button, single_button
from templates.funcs import parse_emoji, get_create_add_info, pack_exists
from templates.media import create_input_file
from templates.const import WATERMARK, COMMON_EMOJI
from templates.types import Answers, texts, texts_buttons

router = Router()

@router.message(ManagingFSM.collecting_emoji_add, F.text, F.chat.type=="private")
async def collecting_emoji_add( \
        message: types.Message,\
        state: FSMContext, \
        bot: Bot, \
        user: baseDB.User \
        ) -> None:

    user = user
        
    answers = Answers(user.lang).get_cancel_btn()
    assert message.text

    match message.text:
        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user.lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user.lang]))
        case _:
            if not parse_emoji(message.text):
                await message.answer(texts["emoji_only_e"][user.lang])
                return
            user["emoji"] = message.text
            await add_sticker(user, bot, message, state)

@router.message(ManagingFSM.collecting_photo_add, F.text, F.chat.type=="private")
async def collecting_photo_add_t( \
        message: types.Message, \
        state: FSMContext, \
        user: baseDB.User \
        ) -> None:
    
    answers = Answers(user.lang).get_cancel_btn()

    match message.text:
        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            user["emoji"] = None
            await message.answer(texts["managing2"][user.lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user.lang]))
        case _:
            await message.answer(texts["image_only_e"][user.lang])

@router.message(ManagingFSM.collecting_photo_add, F.photo | F.sticker, F.chat.type=="private")
async def collecting_photo_add( \
        message: types.Message, \
        state: FSMContext, \
        user: baseDB.User, \
        ) -> None:
    
    await state.set_state(ManagingFSM.collecting_emoji_add)
    if message.photo:
        file_id = message.photo[-1].file_id
        await message.answer(texts["managing0"][user.lang],
            reply_markup=single_button(texts_buttons["cancel"][user.lang][0]))
        await message.answer_photo(file_id,
            caption=texts["managing_add_2"][user.lang],
            reply_markup=COMMON_EMOJI.markup)
    elif message.sticker:
        file_id = message.sticker.file_id
        await message.answer(texts["managing_add_2"][user.lang],
            reply_markup=single_button(texts_buttons["cancel"][user.lang][0]))
        await message.answer_sticker(file_id, reply_markup=COMMON_EMOJI.markup)
    user["image"] = file_id

@router.callback_query(ManagingFSM.collecting_emoji_add, F.data.startswith("emo"))
async def choosing_emoji_query( \
        callback_query: types.CallbackQuery, \
        user: baseDB.User, \
        bot: Bot, \
        state: FSMContext, \
        ) -> None:

    assert callback_query.data and isinstance(callback_query.message, types.Message)

    emoji = callback_query.data[3:]
    user = user
    user["emoji"] = emoji

    await add_sticker(user, bot, callback_query.message, state)

async def add_sticker( \
        user: baseDB.User, \
        bot: Bot, \
        message: types.Message, \
        state: FSMContext, \
        ) -> None:

    file = await create_input_file(bot, user["image"])

    pack_name, pack_name_plus, _, emoji = \
        await get_create_add_info(user)

    if not await pack_exists(bot.get_sticker_set, pack_name_plus):
        await state.set_state(StartFSM.start)
        user.delete_pack()
        user["name"] = None
        user["emoji"] = None
        await message.answer(texts["managing_add_e"][user.lang], \
            reply_markup=start_button(texts_buttons["start"][user.lang], texts_buttons["change_lang"]))
        return

    try:
        
        assert emoji

        if await bot.add_sticker_to_set(int(user.id), pack_name_plus, sticker=types.InputSticker(sticker=file, format="static", emoji_list=parse_emoji(emoji))):
            
            await state.set_state(ManagingFSM.menu)
            user["emoji"] = None

            await message.answer(texts["added1"][user.lang], \
                reply_markup=pack_link_button(texts["created_inline"][user.lang], "https://t.me/addstickers/" + pack_name + str(WATERMARK)))
            await message.answer(texts["created2"][user.lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user.lang]))

    except Exception as e:

        await message.answer(texts["known_e_1"][user.lang]+str(e).split()[-1])

        # temporary
        # update: maybe
        await message.answer(f"""Please send this message to @feddunn\n{type(e).__name__}""")
        
        raise e