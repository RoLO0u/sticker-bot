from typing import Type
from aiogram import Router, F, types

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import StartFSM, JoiningFSM, ManagingFSM
from templates.markups import start_button, managing_button_2
from templates.types import Answers, texts, texts_buttons

router = Router()

@router.message(JoiningFSM.join_pass, F.text, F.chat.type=="private")
async def join_by_password( \
        message: types.Message, \
        state: FSMContext, \
        user: baseDB.User, \
        Pack: Type[baseDB.Pack] \
        ) -> None:

    answers = Answers(user.lang).get_cancel_btn()
    assert message.text

    match message.text:

        case answers.cancel_btn:
            await state.set_state(StartFSM.start)
            await message.answer(texts["cancel"][user.lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user.lang], texts_buttons["change_lang"] ))
    
        case _:
            
            if len(message.text) != 20:
                await message.answer(texts["joining_e1"][user.lang])
                return
            pack = Pack.get_pass(message.text)
            if pack is None:
                await message.answer(texts["joining_e1"][user.lang])                
                return
            if user.id in pack['members']:
                await message.answer(texts["joining_e3"][user.lang])
                return
                
            Pack(pack["packid"]).add_user(user.id)

            await state.set_state(state=StartFSM.start)
            await message.answer(texts["joined"][user.lang], parse_mode="HTML", \
                reply_markup=start_button( texts_buttons["start"][user.lang], texts_buttons["change_lang"] ))

@router.message(JoiningFSM.kick, F.text, F.chat.type=="private")
async def kick_t( \
        message: types.Message, \
        state: FSMContext, \
        user: baseDB.User, \
        Pack: Type[baseDB.Pack], \
        User: Type[baseDB.User] \
        ) -> None:
    
    answers = Answers(user.lang).get_cancel_btn()
    assert message.text

    match message.text:

        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user.lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user.lang]))
            
        case _:
            user_to_kick = User.get_by_username(message.text)
            assert user_to_kick
            pack_id = user.get_chosen()["packid"]
            assert not isinstance(pack_id, list)
            pack = Pack(pack_id)
            
            # user doesn't exists in this pack
            if not pack.includes(id_to_kick := user_to_kick["userid"], ):
                await message.answer(texts["joining_e2"][user.lang])
                return
            # user wants to kick himself
            elif id_to_kick == user.id:
                await message.answer(texts["joining_e4"][user.lang])
                return
            # user wants to kick admin
            elif pack.pack["adm"] == id_to_kick:
                await message.answer(texts["joining_e5"][user.lang])
                return
            
            await state.set_state(ManagingFSM.menu)
            User(id_to_kick).remove_user_from_pack(pack.name)
            await message.answer(texts["kicked"][user.lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user.lang]))