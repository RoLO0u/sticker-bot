from typing import Any, Dict, Union

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from templates import database
from templates.FSM_groups import StartFSM, ManagingFSM, CreatingFSM, JoiningFSM
from templates.markups import start_button, managing_button_inline, single_button
from templates.funcs import delete_non_exist
from templates.const import WATERMARK

router = Router()

@router.message(StartFSM.start, F.text)
async def start_menu(                                   \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        bot: Bot,                                       \
        user_id: str,                                   \
        user_lang: str                                  \
        ) -> Any:
    
    # TODO check packs availibility

    class Answers:
        join_btn = texts["start_buttons"][user_lang][0]
        create_btn = texts["start_buttons"][user_lang][1]
        man_btn = texts["start_buttons"][user_lang][2]
        ch_lan_en, ch_lan_ua = texts["change_lang_buttons"]

    # TODO: make match case better. More: README.md

    match message.text:

        case Answers.join_btn:

            await state.set_state(JoiningFSM.join_pass)

            await message.answer(texts["joining1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))

        case Answers.create_btn:
            
            await state.set_state(CreatingFSM.creating_name)

            await message.answer(texts["creating1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))

        case Answers.man_btn:

            await state.set_state(ManagingFSM.choosing_pack)
            await message.answer(texts["managing0"][user_lang], \
                reply_markup=single_button(texts["back"][user_lang]))

            # Delete pack for db if it was deleted
            await delete_non_exist(bot.get_sticker_set, user_id)

            # user have packs
            if database.get_user_packs_id(user_id):
                await message.answer(texts["managing"][user_lang], \
                    reply_markup=managing_button_inline( list(database.get_user_packs(user_id)) ))
            
            else:
                await message.answer(texts["managing_e"][user_lang])

        case Answers.ch_lan_en|Answers.ch_lan_ua:

            match message.text:
                
                case Answers.ch_lan_en:
                    change_to = "en"
                
                case Answers.ch_lan_ua:
                    change_to = "ua"

            database.change_lang(user_id, change_to)

            await message.answer(texts["lan_changed"][change_to], \
                reply_markup=start_button( texts["start_buttons"][change_to], texts["change_lang_buttons"] ))

        case _:
            await message.answer(texts["unknown_exception_2"][user_lang])