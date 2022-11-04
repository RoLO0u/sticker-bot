from typing import Dict, Any, Union

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates import database
from templates.FSM_groups import StartFSM, ManagingFSM
from templates.markups import start_button, managing_button, managing_button_2, managing_button_inline, cancel_button
from templates.funcs import delete_non_exist, have_stickers
from templates.const import WATERMARK

router = Router()

@router.message(ManagingFSM.choosing_pack, F.text)
async def choosing_pack_t(                              \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        user_lang: str                                  \
        ) -> Any:
    
    class Answers:
        back_btn_en, back_btn_ua, back_btn_is = texts["back"].values()

    match message.text:

        case Answers.back_btn_en | Answers.back_btn_ua | Answers.back_btn_is:

            await state.set_state(StartFSM.start)

            await message.answer(texts["backed"][user_lang],\
                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
            
        case _:
            await message.answer(texts["managing_exception_1"][user_lang])

@router.message(ManagingFSM.menu, F.text)
async def menu(                                         \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        bot: Bot,                                       \
        user_id: str,                                   \
        user_lang: str                                  \
        ) -> Any:

    packs = database.get_user_packs(user_id)
    
    # TODO create inline sticker pick like in @Stickers bot

    class Answers:
        back_btn = texts["managing_buttons_2"][user_lang][-1]
        add_btn = texts["managing_buttons_2"][user_lang][0]
        del_stick_btn = texts["managing_buttons_2"][user_lang][1]
        del_pack_btn = texts["managing_buttons_2"][user_lang][-4]
        show_btn = texts["managing_buttons_2"][user_lang][-2]

    match message.text:
        
        case Answers.back_btn:
            
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

        case Answers.add_btn:
            await state.set_state(ManagingFSM.collecting_emoji_add)
            await message.answer(texts["managing_add_1"][user_lang], \
                reply_markup=cancel_button(texts["cancel_button"][user_lang]))

        case Answers.del_stick_btn:
            await state.set_state(ManagingFSM.collecting_sticker)
            await message.answer(texts["managing_del_1"][user_lang], \
                reply_markup=cancel_button(texts["cancel_button"][user_lang]))
        
        case Answers.del_pack_btn:
            await state.set_state(ManagingFSM.are_you_sure)
            await message.answer(texts["managing_del2_1"][user_lang], parse_mode="markdown", \
                reply_markup=cancel_button(texts["cancel_button"][user_lang]))

        case Answers.show_btn:
            if await have_stickers(database.get_additional_info(user_id)["name"], bot.get_sticker_set):
                sticker = await bot.get_sticker_set(database.get_additional_info(user_id)["name"]+WATERMARK)
                await message.answer_sticker(sticker=sticker.stickers[0].file_id)
            else:
                await message.answer(texts["managing_show_e"][user_lang])

        # TODO this is temporary case                
        case _:
            msg = {"en": "Sorry, we don't have this function now. Use @Stickers to solve problem you have", \
                "ua": "Вибачте, ми не маєм цієї функції наразі. Скористуйтесь @Stickers, щоб вирішити вашу проблему", \
                "is": "Sorry, we don't have this function now. Use @Stickers to solve problem you have"}
            await message.answer(msg[user_lang])

@router.callback_query(F.data, \
    lambda callback_query: callback_query.data in database.get_user_packs_id(str(callback_query.from_user.id)), \
    ManagingFSM.choosing_pack)
async def choosing_pack(\
        callback_query: types.CallbackQuery,            \
        state: FSMContext,                              \
        texts: Dict[str, Dict[str, Union[str, list]]],  \
        # for no idk reason middleware don't work with callback query handlers :<
        ) -> Any:

    user_id = str(callback_query.from_user.id)
    user_lang = database.reg_user(user_id)

    await state.set_state(ManagingFSM.menu)
    database.change_name(user_id, callback_query.data)

    await callback_query.message.answer(texts["managing2"][user_lang], \
        reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))