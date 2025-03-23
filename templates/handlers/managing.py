from typing import Type

from aiogram import types, Router, Bot, F

from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from templates.database import baseDB
from templates.FSM_groups import StartFSM, ManagingFSM, JoiningFSM, ChangeStickerFSM
from templates.markups import start_button, managing_button_2, packs_inline, single_button, kick_member_button
from templates.funcs import delete_non_existent, has_stickers, random_string
from templates.const import WATERMARK
from templates.types import Answers, texts, texts_buttons

router = Router()

def callback_query_filter(callback_query: types.CallbackQuery, User: Type[baseDB.User]) -> bool:
    return callback_query.data in User(str(callback_query.from_user.id))["packs"]

@router.message(ManagingFSM.choosing_pack, F.text, F.chat.type=="private")
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

@router.message(ManagingFSM.menu, F.text, F.chat.type=="private")
async def menu( \
        message: types.Message, \
        state: FSMContext, \
        bot: Bot, \
        user: baseDB.User, \
        User: Type[baseDB.User] \
        ) -> None:

    # TODO create inline sticker pick like in @Stickers bot

    answers = Answers(user.lang).get_menu_btns()

    match message.text:
        
        case answers.back_btn:
            
            await state.set_state(ManagingFSM.choosing_pack)
            await message.answer(texts["managing0"][user.lang], \
                reply_markup=single_button(texts["back"][user.lang]))

            # Delete pack for db if it was deleted
            await delete_non_existent(bot.get_sticker_set, user)
        
            # user have packs
            if user["packs"]:
                await message.answer(texts["managing"][user.lang], \
                    reply_markup=packs_inline(list(user.get_packs()), texts_buttons["start"][user.lang][1]))
            
            else:
                await message.answer(texts["managing_e"][user.lang])

        case answers.add_btn:
            await state.set_state(ManagingFSM.collecting_photo_add)
            await message.answer(texts["managing_add_1"][user.lang], \
                reply_markup=single_button(texts["cancel_button"][user.lang]))

        case answers.del_stick_btn:
            await state.set_state(ManagingFSM.collecting_sticker)
            await message.answer(texts["managing_del_1"][user.lang], \
                reply_markup=single_button(texts["cancel_button"][user.lang]))
        
        case answers.del_pack_btn:
            await state.set_state(ManagingFSM.are_you_sure)
            await message.answer(texts["managing_del2_1"][user.lang], parse_mode="markdown", \
                reply_markup=single_button(texts["cancel_button"][user.lang]))

        case answers.show_btn:
            pack_name = user["name"]
            assert pack_name
            if await has_stickers(pack_name, bot.get_sticker_set):
                sticker = await bot.get_sticker_set(pack_name+str(WATERMARK))
                await message.answer_sticker(sticker=sticker.stickers[0].file_id)
            else:
                await message.answer(texts["managing_show_e"][user.lang])
        
        case answers.invite_btn:
            pack = user.get_chosen()
            assert pack
            assert not isinstance(pack["packid"], list) and not isinstance(pack["password"], list)
            token = pack["packid"]+pack["password"]
            await message.answer(texts["how_to_invite"][user.lang].format(token), parse_mode="markdown")

        case answers.kick_btn:
            pack = user.get_chosen()
            assert pack
            members = []
            for member_id in pack["members"]:
                member = User(member_id)
                if member.id in (user.id, pack["adm"]):
                    continue
                members.append(member)

            if not members:
                await message.answer(texts["kick_e"][user.lang])
                return

            await message.answer(texts["kick"][user.lang], \
                reply_markup=kick_member_button(members))
            
        case answers.edit_emoji_btn:
            await state.set_state(ChangeStickerFSM.change_sticker_emoji)
            await message.answer(texts["managing_emoji_1"][user.lang], \
                reply_markup=single_button(texts["cancel_button"][user.lang]))
            
        case answers.set_pack_title:
            await state.set_state(ManagingFSM.set_title)
            await message.answer(texts["managing_title_1"][user.lang], \
                reply_markup=single_button(texts["cancel_button"][user.lang]))
        case answers.generate_password:
            pack = user.get_chosen()
            assert pack
            pack["password"] = random_string()
            await message.answer(texts["new_password_generated"][user.lang].format(f"{pack['packid']}{pack['password']}"),
                parse_mode=ParseMode.MARKDOWN_V2)

@router.callback_query(F.data, \
    ManagingFSM.choosing_pack, \
    callback_query_filter)
async def choosing_pack(\
        callback_query: types.CallbackQuery, \
        state: FSMContext, \
        user: baseDB.User \
        ) -> None:

    user_id = str(callback_query.from_user.id)
    assert callback_query.from_user.username
    user_lang = user.register(user_id, callback_query.from_user.username, first_name=callback_query.from_user.first_name)

    await state.set_state(ManagingFSM.menu)
    user["name"] = callback_query.data

    assert isinstance(callback_query.message, types.Message)
    await callback_query.message.answer(texts["managing2"][user_lang], \
        reply_markup=managing_button_2(texts_buttons["managing_2"][user_lang]))
    
@router.message(ManagingFSM.set_title, F.text, F.chat.type=="private")
async def set_title( \
        message: types.Message, \
        state: FSMContext, \
        bot: Bot, \
        user: baseDB.User, \
        Pack: Type[baseDB.Pack] \
        ) -> None:
    
    answers = Answers(user.lang).get_cancel_btn()
    assert message.text
    match message.text:
        case answers.cancel_btn:
            await state.set_state(ManagingFSM.menu)
            await message.answer(texts["managing2"][user.lang], \
                reply_markup=managing_button_2(texts_buttons["managing_2"][user.lang]))
        case _ if len(message.text) < 64:
            pack_id = user["name"]
            assert pack_id
            if await bot.set_sticker_set_title(pack_id+str(WATERMARK), message.text):
                Pack(pack_id).change("title", message.text)
                await state.set_state(ManagingFSM.menu)
                await message.answer(texts["managed_title"][user.lang], \
                    reply_markup=managing_button_2(texts_buttons["managing_2"][user.lang]))
        case _:
            await message.answer(texts["naming_e1"][user.lang])