from typing import Type
from aiogram import Router, F, types

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import StartFSM, JoiningFSM, ManagingFSM
from templates.markups import start_button, managing_button_2
from templates.types import Answers, texts, texts_buttons
from templates.Exceptions import NotFoundException

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
            try:
                pack = Pack.get_pass(message.text)
            except NotFoundException:
                await message.answer(texts["pack_doesnt_exist_e"][user.lang])
                return
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

@router.callback_query(F.data.startswith("kick"))
async def kick_t( \
        callback_query: types.CallbackQuery, \
        state: FSMContext, \
        user: baseDB.User, \
        Pack: Type[baseDB.Pack], \
        User: Type[baseDB.User] \
        ) -> None:
    
    assert callback_query.data and callback_query.message
    
    user_to_kick = callback_query.data[4:]
    assert user_to_kick
    pack = user.get_chosen()
    if not pack:
        await callback_query.message.answer(texts["pack_not_chosen"][user.lang])
        return
    assert not isinstance(pack.name, list)
    
    # user doesn't exist in this pack
    if not pack.includes(user_to_kick):
        await callback_query.message.answer(texts["joining_e2"][user.lang])
        return
    
    await state.set_state(ManagingFSM.menu)
    User(user_to_kick).remove_from_pack(pack.name)
    await callback_query.message.answer(texts["kicked"][user.lang], \
        reply_markup=managing_button_2(texts_buttons["managing_2"][user.lang]))