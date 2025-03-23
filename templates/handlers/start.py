from typing import Any, Type

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import StartFSM, ManagingFSM, CreatingFSM, JoiningFSM
from templates.markups import start_button, packs_inline, single_button, create_options
from templates.funcs import delete_non_existent
from templates.types import Answers, texts, texts_buttons

router = Router()

@router.message(StartFSM.start, F.text, F.chat.type=="private")
async def start_menu( \
        message: types.Message, \
        state: FSMContext, \
        bot: Bot, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> None:
    
    # TODO check packs availibility

    answers = Answers(user_lang).get_start_btns()
    # TODO: make match case better. More: README.md

    match message.text:

        case answers.join_btn:

            await state.set_state(JoiningFSM.join_pass)

            await message.answer(texts["joining1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))

        case answers.create_btn:
            
            await state.set_state(CreatingFSM.choosing_option)

            await message.answer(texts["start_opts"][user_lang], \
                reply_markup=create_options(texts_buttons["start_opts"][user_lang]))

        case answers.man_btn:

            await state.set_state(ManagingFSM.choosing_pack)
            await message.answer(texts["managing0"][user_lang], \
                reply_markup=single_button(texts["back"][user_lang]))

            # Delete pack for db if it was deleted
            await delete_non_existent(bot.get_sticker_set, User, user_id)

            # user have packs
            user = User(user_id)
            if user["packs"]:
                await message.answer(texts["managing"][user_lang], \
                    reply_markup=packs_inline(list(user.get_packs()), texts_buttons["start"][user_lang][1]))
            
            else:
                await message.answer(texts["managing_e"][user_lang])

        case answers.ch_lan_en|answers.ch_lan_ua:

            match message.text:
                case answers.ch_lan_en:
                    change_to = "en"
                case answers.ch_lan_ua:
                    change_to = "ua"
                case _:
                    raise NotImplementedError("No implementation when user clicked on other change language than 'en' or 'ua'")

            User(user_id)["language"] = change_to

            await message.answer(texts["lan_changed"][change_to], \
                reply_markup=start_button( texts_buttons["start"][change_to], texts_buttons["change_lang"] ))

        case _:
            await message.answer(texts["unknown_exception_2"][user_lang])