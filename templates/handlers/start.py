from typing import Any, Dict, Union

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from templates import database
from templates.FSM_groups import StartFSM, ManagingFSM, CreatingFSM, JoiningFSM
from templates.markups import managing_button, start_button, cancel_button, managing_button_inline
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

    answers = list(zip(*texts["start_buttons"].values())) + [texts["change_lang_buttons"]] # -> [('Join pack', 'Приєднатись до пакунку'), ('Create pack', 'Створити пакунок'), ('Add sticker', 'Додати наліпку'), ["Change language to 🇬🇧 (English)", "Змінити мову на 🇺🇦 (Українську)"]]

    class Answers:
        join_btn_en, join_btn_ua, join_btn_is = answers[0]
        create_btn_en, create_btn_ua, create_btn_is = answers[1]
        man_btn_en, man_btn_ua, man_btn_is = answers[2]
        ch_lan_en, ch_lan_ua, ch_lan_is = answers[3]

    # TODO: make match case better. More: README.md

    match message.text:

        case Answers.join_btn_en|Answers.join_btn_ua|Answers.join_btn_is:

            await message.answer(texts["joined"][user_lang], \
                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

        case Answers.create_btn_en|Answers.create_btn_ua|Answers.create_btn_is:
            
            await state.set_state(CreatingFSM.creating_name)

            await message.answer(texts["creating1"][user_lang], \
                reply_markup=cancel_button(texts["cancel_button"][user_lang]))

        case Answers.man_btn_en|Answers.man_btn_ua|Answers.man_btn_is:

            await state.set_state(ManagingFSM.choosing_pack)
            await message.answer(texts["managing0"][user_lang], \
                reply_markup=managing_button(texts["back"][user_lang]))

            # Delete pack for db if it was deleted
            await delete_non_exist(bot.get_sticker_set, user_id)

            # user have packs
            if database.get_user_packs_id(user_id):
                await message.answer(texts["managing"][user_lang], \
                    reply_markup=managing_button_inline( list(database.get_user_packs(user_id)) ))
            
            else:
                await message.answer(texts["managing_e"][user_lang])

        case Answers.ch_lan_en|Answers.ch_lan_ua|Answers.ch_lan_is:

            match message.text:
                
                case Answers.ch_lan_en:
                    change_to = "en"
                
                case Answers.ch_lan_ua:
                    change_to = "ua"

                case Answers.ch_lan_is:
                    change_to = "is"

            database.change_lang(user_id, change_to)

            await message.answer(texts["lan_changed"][change_to], \
                reply_markup=start_button( texts["start_buttons"][change_to], texts["change_lang_buttons"] ))

        case _:
            await message.answer(texts["unknown_exception_2"][user_lang])