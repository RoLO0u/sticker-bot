from typing import Any, Type

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import StartFSM, ManagingFSM
from templates.markups import start_button, managing_button_2
from templates.const import WATERMARK
from templates.types import Texts, TextsButtons

router = Router()

@router.message(ManagingFSM.collecting_sticker, F.sticker)
async def delete_sticker_from_pack(                     \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        bot: Bot,                                       \
        user_id: str,                                   \
        user_lang: str,                                 \
        User: Type[baseDB.User]                         \
        ) -> Any:

    await state.set_state(StartFSM.start)

    # router already has filter on sticker
    sticker_id = message.sticker.file_id # type: ignore
    unique_id = message.sticker.file_unique_id # type: ignore

    # TODO: make warning message if it's last sticker

    name = User(user_id).get_additional_info()["name"]
    assert name is not None
    sticker_set = await bot.get_sticker_set(name+WATERMARK)
    stickers_un_id = [sticker.file_unique_id for sticker in sticker_set.stickers]

    # checking if sticker in user stickerpack
    if unique_id in stickers_un_id:

        await bot.delete_sticker_from_set(sticker_id)

        await message.answer(texts["deleted"][user_lang], \
            reply_markup=start_button(texts_buttons["start"][user_lang], texts_buttons["change_lang"]))
    
    else:
        await message.answer(texts["managing_del_e"][user_lang])

@router.message(ManagingFSM.collecting_sticker, F.text)
async def delete_sticker_from_pack_t(                   \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        user_lang: str                                  \
        ) -> Any:

    class Answers:
        cancel_btn = texts_buttons["cancel"][user_lang][0]

    match message.text:

        case Answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))

        case _:
            await message.answer(texts["sticker_only_e"][user_lang])

@router.message(ManagingFSM.are_you_sure, F.text)
async def confirming_pack_deleting(                     \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        bot: Bot,                                       \
        user_id: str,                                   \
        user_lang: str,                                 \
        User: Type[baseDB.User]                         \
        ) -> Any:
    
    class Answers:
        cancel_btn = texts_buttons["cancel"][user_lang][0]
        confirming = texts["confirming"][user_lang]

    match message.text:

        case Answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))

        case Answers.confirming:

            await state.set_state(StartFSM.start)

            user = User(user_id)
            set_name = user.get_additional_info()["name"]
            assert set_name is not None

            sticker_set = await bot.get_sticker_set(set_name+WATERMARK)

            for sticker in sticker_set.stickers:
                await bot.delete_sticker_from_set(sticker.file_id)

            user.delete_pack()

            await message.answer(texts["pack_deleted"][user_lang], \
                reply_markup=start_button(texts_buttons["start"][user_lang], texts_buttons["change_lang"]))

        case _:
            await message.answer(texts["unknown_exception_2"][user_lang])