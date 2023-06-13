from typing import Any

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates import database
from templates.FSM_groups import StartFSM, ManagingFSM, JoiningFSM
from templates.markups import start_button, managing_button_2, managing_button_inline, single_button
from templates.funcs import delete_non_exist, have_stickers
from templates.const import WATERMARK
from templates.types import Texts, TextsButtons

router = Router()

@router.message(ManagingFSM.choosing_pack, F.text)
async def choosing_pack_t(                              \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        user_lang: str                                  \
        ) -> Any:
    
    class Answers:
        back_btn_en, back_btn_ua = texts["back"].values()

    match message.text:

        case Answers.back_btn_en | Answers.back_btn_ua:

            await state.set_state(StartFSM.start)

            texts["backed"][user_lang]

            await message.answer(texts["backed"][user_lang],\
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))
            
        case _:
            await message.answer(texts["managing_exception_1"][user_lang])

@router.message(ManagingFSM.menu, F.text)
async def menu(                                         \
        message: types.Message,                         \
        state: FSMContext,                              \
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        bot: Bot,                                       \
        user_id: str,                                   \
        user_lang: str                                  \
        ) -> Any:

    # TODO create inline sticker pick like in @Stickers bot

    class Answers:
        back_btn = texts_buttons["managing_2"][user_lang][-1]
        add_btn = texts_buttons["managing_2"][user_lang][0]
        del_stick_btn = texts_buttons["managing_2"][user_lang][1]
        del_pack_btn = texts_buttons["managing_2"][user_lang][-4]
        show_btn = texts_buttons["managing_2"][user_lang][-2]
        invite_btn = texts_buttons["managing_2"][user_lang][4]
        kick_btn = texts_buttons["managing_2"][user_lang][5]

    match message.text:
        
        case Answers.back_btn:
            
            await state.set_state(ManagingFSM.choosing_pack)
            await message.answer(texts["managing0"][user_lang], \
                reply_markup=single_button(texts["back"][user_lang]))

            # Delete pack for db if it was deleted
            await delete_non_exist(bot.get_sticker_set, user_id)
        
            # user have packs
            user = database.User(user_id)
            if user.get_packs_id():
                await message.answer(texts["managing"][user_lang], \
                    reply_markup=managing_button_inline( list(user.get_packs()) ))
            
            else:
                await message.answer(texts["managing_e"][user_lang])

        # TODO somehow unite next 3 cases (very similar looks)

        case Answers.add_btn:
            await state.set_state(ManagingFSM.collecting_emoji_add)
            await message.answer(texts["managing_add_1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))

        case Answers.del_stick_btn:
            await state.set_state(ManagingFSM.collecting_sticker)
            await message.answer(texts["managing_del_1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))
        
        case Answers.del_pack_btn:
            await state.set_state(ManagingFSM.are_you_sure)
            await message.answer(texts["managing_del2_1"][user_lang], parse_mode="markdown", \
                reply_markup=single_button(texts["cancel_button"][user_lang]))

        case Answers.show_btn:
            pack_name = database.User(user_id).get_additional_info()["name"]
            assert pack_name is not None
            if await have_stickers(pack_name, bot.get_sticker_set):
                sticker = await bot.get_sticker_set(pack_name+WATERMARK)
                await message.answer_sticker(sticker=sticker.stickers[0].file_id)
            else:
                await message.answer(texts["managing_show_e"][user_lang])
        
        case Answers.invite_btn:
            token = database.User(user_id).get_chosen()
            assert not isinstance(token["packid"], list) and not isinstance(token["password"], list)
            token = token["packid"]+token["password"]
            await message.answer(texts["how_to_invite"][user_lang].format(token), parse_mode="markdown")

        case Answers.kick_btn:
            await state.set_state(JoiningFSM.kick)
            await message.answer(texts["kick"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))

        # TODO this is temporary case                
        case _:
            msg = {"en": "Sorry, we don't have this function now. Use @Stickers to solve problem you have", \
                "ua": "Вибачте, ми не маєм цієї функції наразі. Скористуйтесь @Stickers, щоб вирішити вашу проблему"}
            await message.answer(msg[user_lang])

@router.callback_query(F.data, \
    lambda callback_query: callback_query.data in database.User(str(callback_query.from_user.id)).get_packs_id(), \
    ManagingFSM.choosing_pack)
async def choosing_pack(\
        callback_query: types.CallbackQuery,            \
        state: FSMContext,                              \
        texts: Texts,                                   \
        texts_buttons: TextsButtons,                    \
        # for no idk reason middleware don't work with callback query handlers :<
        ) -> Any:

    user_id = str(callback_query.from_user.id)
    assert callback_query.from_user.username is not None
    user_lang = database.User.register(user_id, callback_query.from_user.username)

    await state.set_state(ManagingFSM.menu)
    database.User(user_id).change_name(callback_query.data)

    assert callback_query.message is not None
    await callback_query.message.answer(texts["managing2"][user_lang], \
        reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))