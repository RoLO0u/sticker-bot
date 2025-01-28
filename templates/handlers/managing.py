from typing import Any, Type

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext

from templates.database import baseDB
from templates.FSM_groups import StartFSM, ManagingFSM, JoiningFSM, ChangeStickerFSM
from templates.markups import start_button, managing_button_2, managing_button_inline, single_button
from templates.funcs import delete_non_exist, have_stickers
from templates.const import WATERMARK
from templates.types import Answers, texts, texts_buttons

router = Router()

def callback_query_filter(callback_query: types.CallbackQuery, User: Type[baseDB.User]) -> bool:
    return callback_query.data in User(str(callback_query.from_user.id)).get_packs_id()

@router.message(ManagingFSM.choosing_pack, F.text)
async def choosing_pack_t( \
        message: types.Message, \
        state: FSMContext, \
        user_lang: str \
        ) -> None:
    
    answers = Answers(user_lang).get_back_btns()

    match message.text:

        case answers.back_btn_en | answers.back_btn_ua:
            await state.set_state(StartFSM.start)
            await message.answer(texts["backed"][user_lang],\
                reply_markup=start_button( texts_buttons["start"][user_lang], texts_buttons["change_lang"] ))
            
        case _:
            await message.answer(texts["managing_exception_1"][user_lang])

@router.message(ManagingFSM.menu, F.text)
async def menu( \
        message: types.Message, \
        state: FSMContext, \
        bot: Bot, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User] \
        ) -> None:

    # TODO create inline sticker pick like in @Stickers bot

    answers = Answers(user_lang).get_menu_btns()

    match message.text:
        
        case answers.back_btn:
            
            await state.set_state(ManagingFSM.choosing_pack)
            await message.answer(texts["managing0"][user_lang], \
                reply_markup=single_button(texts["back"][user_lang]))

            # Delete pack for db if it was deleted
            await delete_non_exist(bot.get_sticker_set, User, user_id)
        
            # user have packs
            user = User(user_id)
            if user.get_packs_id():
                await message.answer(texts["managing"][user_lang], \
                    reply_markup=managing_button_inline( list(user.get_packs()) ))
            
            else:
                await message.answer(texts["managing_e"][user_lang])

        case answers.add_btn:
            await state.set_state(ManagingFSM.collecting_emoji_add)
            await message.answer(texts["managing_add_1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))

        case answers.del_stick_btn:
            await state.set_state(ManagingFSM.collecting_sticker)
            await message.answer(texts["managing_del_1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))
        
        case answers.del_pack_btn:
            await state.set_state(ManagingFSM.are_you_sure)
            await message.answer(texts["managing_del2_1"][user_lang], parse_mode="markdown", \
                reply_markup=single_button(texts["cancel_button"][user_lang]))

        case answers.show_btn:
            pack_name = User(user_id)["name"]
            assert pack_name
            if await have_stickers(pack_name, bot.get_sticker_set):
                sticker = await bot.get_sticker_set(pack_name+str(WATERMARK))
                await message.answer_sticker(sticker=sticker.stickers[0].file_id)
            else:
                await message.answer(texts["managing_show_e"][user_lang])
        
        case answers.invite_btn:
            token = User(user_id).get_chosen()
            assert not isinstance(token["packid"], list) and not isinstance(token["password"], list)
            token = token["packid"]+token["password"]
            await message.answer(texts["how_to_invite"][user_lang].format(token), parse_mode="markdown")

        case answers.kick_btn:
            await state.set_state(JoiningFSM.kick)
            await message.answer(texts["kick"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))
            
        case answers.edit_emoji_btn:
            await state.set_state(ChangeStickerFSM.change_sticker_emoji)
            await message.answer(texts["managing_emoji_1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))
            
        case answers.set_pack_title:
            await state.set_state(ManagingFSM.set_title)
            await message.answer(texts["managing_title_1"][user_lang], \
                reply_markup=single_button(texts["cancel_button"][user_lang]))

        # TODO this is temporary case
        case _:
            msg = {"en": "Sorry, we don't have this function now. Use @Stickers to solve problem you have", \
                "ua": "Вибачте, ми не маєм цієї функції наразі. Скористуйтесь @Stickers, щоб вирішити вашу проблему"}
            await message.answer(msg[user_lang])

@router.callback_query(F.data, \
    ManagingFSM.choosing_pack, \
    callback_query_filter)
async def choosing_pack(\
        callback_query: types.CallbackQuery, \
        state: FSMContext, \
        User: Type[baseDB.User] \
        ) -> None:

    user_id = str(callback_query.from_user.id)
    assert callback_query.from_user.username
    user_lang = User.register(user_id, callback_query.from_user.username)

    await state.set_state(ManagingFSM.menu)
    User(user_id).change_name(callback_query.data)

    assert isinstance(callback_query.message, types.Message)
    await callback_query.message.answer(texts["managing2"][user_lang], \
        reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))
    
@router.message(ManagingFSM.set_title, F.text)
async def set_title( \
        message: types.Message, \
        state: FSMContext, \
        bot: Bot, \
        user_id: str, \
        user_lang: str, \
        User: Type[baseDB.User], \
        Pack: Type[baseDB.Pack]
        ) -> None:
    
    answers = Answers(user_lang).get_cancel_btn()
    assert message.text
    match message.text:
        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user_lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))
        case _ if len(message.text) < 64:
            pack_id = User(user_id)["name"]
            assert pack_id
            if await bot.set_sticker_set_title(pack_id+str(WATERMARK), message.text):
                Pack(pack_id).change("title", message.text)
                await state.set_state(ManagingFSM.menu)
                await message.answer(texts["managed_title"][user_lang], \
                    reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))
        case _:
            await message.answer(texts["naming_e1"][user_lang])