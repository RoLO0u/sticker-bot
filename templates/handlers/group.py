from typing import Dict, Union, Any
from aiogram import Router, F, types

from aiogram.fsm.context import FSMContext

from templates import database
from templates.FSM_groups import StartFSM, JoiningFSM
from templates.markups import start_button

router = Router()

@router.message(JoiningFSM.join_pass, F.text)
async def join_by_password(                             \
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
    
        case _:

            if (pack := database.get_pack_pass(message.text)) and (len(message.text) == 20):

                database.add_user(user_id, pack["packid"])

                await state.set_state(StartFSM.start)
                await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                    reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

            else:
                await message.answer(texts["joining_e1"][user_lang])

@router.message(JoiningFSM.kick, F.text)
async def kick_t(                                       \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        user_id: str,                                    \
        user_lang: str                                  \
        ) -> Any:
    
    class Answers:
        cancel_btn = texts["cancel_button"][user_lang]

    match message.text:

        case Answers.cancel_btn:
            
            await state.set_state(StartFSM.start)
            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
        
        case _:

            if database.in_pack(user_kick := database.get_user_by_uname(message.text)["userid"], pack := database.get_choosen_pack(user_id)["packid"]) and user_kick != user_id:

                await state.set_state(StartFSM.start)
                database.remove_user_from_pack(user_kick, pack)
                await message.answer(texts["kicked"][user_lang], \
                    reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

            else:
                await message.answer(texts["joining_e2"][user_lang])