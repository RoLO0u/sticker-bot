from typing import Any, Type
from aiogram import Router, F, types

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import StartFSM, JoiningFSM
from templates.markups import start_button
from templates.types import Texts, TextsButtons

router = Router()

@router.message(JoiningFSM.join_pass, F.text)
async def join_by_password(                             \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        user_id: str,                                   \
        user_lang: str,                                 \
        Pack: Type[baseDB.Pack]                         \
        ) -> Any:

    class Answers:
        cancel_btn = texts_buttons["cancel"][user_lang][0]
    assert message.text is not None

    match message.text:

        case Answers.cancel_btn:
            await state.set_state(StartFSM.start)
            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))
    
        case _:
            
            if len(message.text) != 20:
                await message.answer(texts["joining_e1"][user_lang])
                return
            pack = Pack.get_pass(message.text)
            if pack is None:
                await message.answer(texts["joining_e1"][user_lang])                
                return
            if user_id in pack['members']:
                await message.answer(texts["joining_e3"][user_lang])
                return
                
            Pack(pack["packid"]).add_user(user_id)

            await state.set_state(state=StartFSM.start)
            await message.answer(texts["joined"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))

@router.message(JoiningFSM.kick, F.text)
async def kick_t(                                       \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        user_id: str,                                   \
        user_lang: str,                                 \
        MiscDB: Type[baseDB.MiscDB],                    \
        User: Type[baseDB.User],                        \
        Pack: Type[baseDB.Pack]                         \
        ) -> Any:
    
    class Answers:
        cancel_btn = texts_buttons["cancel"][user_lang][0]
    assert message.text is not None

    match message.text:

        case Answers.cancel_btn:
            
            await state.set_state(StartFSM.start)
            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))
        
        case _:
            
            user_to_kick = User.get_by_username(message.text)
            assert user_to_kick is not None
            pack_id = User(user_id).get_chosen()["packid"]
            assert not isinstance(pack_id, list)

            if Pack(pack_id).include(user_kick := user_to_kick["userid"], ) and user_kick != user_id:

                await state.set_state(StartFSM.start)
                User(user_kick).remove_user_from_pack(pack_id)
                await message.answer(texts["kicked"][user_lang], \
                    reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))

            else:
                await message.answer(texts["joining_e2"][user_lang])