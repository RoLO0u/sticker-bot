from typing import Any, Dict, Union

from aiogram import types, Router, Bot, F
from aiogram.filters import Command
from aiogram.utils.markdown import hide_link
from aiogram.fsm.context import FSMContext

from templates import database, markups
from templates.FSM_groups import StartFSM

router = Router()

@router.message(Command("start"))
async def start(                                \
        message: types.Message,                 \
        state: FSMContext,                      \
        texts:                                  \
        Dict[str, Dict[str, Union[str, list]]], \
        user_lang: str                          \
        ) -> Any:
    
    await state.set_state(StartFSM.start)

    await message.answer(texts["start"][user_lang], parse_mode="HTML", \
        reply_markup=markups.start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
    
@router.message(Command("help"))
async def help(                                        \
        message: types.Message,                        \
        texts: Dict[str, Dict[str, Union[str, list]]], \
        user_lang: str                                 \
        ) -> Any:

    await message.answer(f"{hide_link('https://i.imgur.com/ZRv0bDC.png')}"
        f"{texts['help_1'][user_lang]}", parse_mode="HTML")

@router.message(Command("test"), F.chat.id == 602197013)
async def test(                 \
        message: types.Message, \
        bot: Bot,               \
        ) -> Any:
    to_check = 8
    match to_check:
        case 0:
            await bot.get_sticker_set(message.get_args())
            print(1)
        case 1:
            await bot.send_sticker(message.chat.id, \
                await bot.download_file( bot.get_file(bot.get_sticker_set("hxxhzkhRpq_by_paces_bot").stickers[0].file_id).file_path))
        case 2:
            await bot.send_sticker(chat_id=message.chat.id, sticker=bot.get_sticker_set("hxxhzkhRpq_by_paces_bot").stickers[0].file_id)
        case 3:
            await bot.send_sticker(chat_id=message.chat.id, sticker="CAACAgIAAxUAAWMtsh1VasOoVWxE67jLt5UBaQkNAAIqIQACF7xxSVCXRGA5ki1uKQQ")
        case 4:
            await message.answer(database.get_user_info(f"{message.from_user.id}"))
        case 5:
            database.change_status(f"{message.from_user.id}", "start")
        case 6:
            database.get_user_packs_id(f"{message.from_user.id}")
        case 7:
            database.get_all_packs()
        case 8:
            print(message.parse_entities())
            message.answer(message.parse_entities(), reply_markup="HTML")