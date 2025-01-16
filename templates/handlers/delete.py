from typing import Any, Type

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import StartFSM, ManagingFSM
from templates.markups import start_button, managing_button_2, managing_del_conf
from templates.const import WATERMARK
from templates.types import Answers, texts, texts_buttons

router = Router()

@router.message(ManagingFSM.collecting_sticker, F.sticker)
async def delete_sticker_from_pack( \
        message: types.Message, \
        state: FSMContext, \
        bot: Bot, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> None:

    # router already has filter on sticker
    assert message.sticker
    sticker_id = message.sticker.file_id
    unique_id = message.sticker.file_unique_id

    user = User(user_id)
    name = user["name"]
    assert name
    sticker_set = await bot.get_sticker_set(name+str(WATERMARK))
    stickers_un_id = [sticker.file_unique_id for sticker in sticker_set.stickers]

    # checking if sticker in user stickerpack
    if not unique_id in stickers_un_id:
        await message.answer(texts["managing_del_e"][user_lang])
        return
    if len(stickers_un_id) <= 1:
        await state.set_state(ManagingFSM.delete_sticker)
        user.change("sticker", sticker_id)
        await message.answer(texts["managing_del_conf"][user_lang],
            reply_markup=managing_del_conf(texts_buttons["managing_del_conf"][user_lang]))
        return
    
    await state.set_state(ManagingFSM.menu)
    await bot.delete_sticker_from_set(sticker_id)
    await message.answer(texts["deleted"][user_lang], \
        reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))    

@router.message(ManagingFSM.delete_sticker, F.text)
async def confirm_delete_sticker( \
        message: types.Message, \
        state: FSMContext, \
        bot: Bot, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> None:
    
    answers = Answers(user_lang).get_cancel_btn() \
        .get_delete_sticker_confirming()

    match message.text:
        
        case answers.delete_sticker_confirming:
            user = User(user_id)
            sticker_id = user["sticker"]
            set_name = user["name"]
            assert sticker_id and set_name
            await state.set_state(StartFSM.start)
            await bot.delete_sticker_set(set_name+str(WATERMARK))
            await message.answer(texts["deleted"][user_lang], \
                reply_markup=start_button(texts_buttons["start"][user_lang], texts_buttons["change_lang"]))
        
        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))

        case _:
            await message.answer(texts["unknown_exception_2"][user_lang])   

@router.message(ManagingFSM.collecting_sticker, F.text)
async def delete_sticker_from_pack_t( \
        message: types.Message, \
        state: FSMContext, \
        user_lang: str 
        ) -> None:

    answers = Answers(user_lang).get_cancel_btn()
    
    match message.text:
        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))
        case _:
            await message.answer(texts["sticker_only_e"][user_lang])

@router.message(ManagingFSM.are_you_sure, F.text)
async def confirming_pack_deleting( \
        message: types.Message, \
        state: FSMContext, \
        bot: Bot, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> None:
    
    answers = Answers(user_lang).get_cancel_btn().get_confirming()

    match message.text:

        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))

        case answers.confirming:

            await state.set_state(StartFSM.start)

            user = User(user_id)
            set_name = user["name"]
            assert set_name

            # sticker_set = await bot.get_sticker_set(set_name+str(WATERMARK))

            # for sticker in sticker_set.stickers:
            #     await bot.delete_sticker_from_set(sticker.file_id)

            await bot.delete_sticker_set(set_name+str(WATERMARK))
            user.delete_pack()

            await message.answer(texts["pack_deleted"][user_lang], \
                reply_markup=start_button(texts_buttons["start"][user_lang], texts_buttons["change_lang"]))

        case _:
            await message.answer(texts["unknown_exception_4"][user_lang])