from typing import Dict, Any, Union

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates import database
from templates.FSM_groups import StartFSM, ManagingFSM
from templates.markups import start_button, managing_button, managing_button_2, managing_button_inline, cancel_button
from templates.funcs import delete_non_exist, have_stickers
from templates.const import WATERMARK

router = Router()

@router.message(ManagingFSM.collecting_sticker, F.sticker)
async def delete_sticker_from_pack(                     \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        bot: Bot,                                       \
        user_id: str,                                   \
        user_lang: str                                  \
        ) -> Any:

    await state.set_state(StartFSM.start)

    sticker_id = message.sticker.file_id
    unique_id = message.sticker.file_unique_id

    # TODO: make warning message if it's last sticker

    sticker_set = await bot.get_sticker_set(database.get_additional_info(user_id)["name"]+WATERMARK)
    stickers_un_id = [sticker.file_unique_id for sticker in sticker_set.stickers]

    # checking if sticker in user stickerpack
    if unique_id in stickers_un_id:

        pack_name = database.get_additional_info(user_id)["name"]

        await bot.delete_sticker_from_set(sticker_id)

        await message.answer(texts["deleted"][user_lang], \
            reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))
    
    else:
        await message.answer(texts["managing_del_e"][user_lang])

@router.message(ManagingFSM.collecting_sticker, F.text)
async def delete_sticker_from_pack_t(                   \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
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
            await message.answer(texts["sticker_only_e"][user_lang])

@router.message(ManagingFSM.are_you_sure, F.text)
async def confirming_pack_deleting(                     \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        bot: Bot,                                       \
        user_id: str,                                   \
        user_lang: str                                  \
        ) -> Any:
    
    class Answers:
        cancel_btn = texts["cancel_button"][user_lang]
        confirming = texts["confirming"][user_lang]

    match message.text:

        case Answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))

        case Answers.confirming:

            await state.set_state(StartFSM.start)

            set_name = database.get_additional_info(user_id)["name"]

            sticker_set = await bot.get_sticker_set(set_name+WATERMARK)

            for sticker in sticker_set.stickers:
                await bot.delete_sticker_from_set(sticker.file_id)

            database.delete_pack(user_id, set_name)
            database.change_name(user_id, None)

            await message.answer(texts["pack_deleted"][user_lang], \
                reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))

        case _:
            await message.answer(texts["unknown_exception_2"][user_lang])