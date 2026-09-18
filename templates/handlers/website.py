from aiogram import types, Router, Bot, F
from aiogram.filters import Command
from aiogram.utils.markdown import hide_link
from aiogram.fsm.context import FSMContext

from templates import markups, const
from templates.database import baseDB
from templates.FSM_groups import StartFSM
from templates.types import texts, texts_buttons

router = Router()

@router.message(Command("connect"), F.chat.type=="private")
async def connect( \
        message: types.Message, \
        user: baseDB.User, \
        MiscDB: type[baseDB.MiscDB], \
        ) -> None:

    if user["email"]:
        await message.answer(texts["connected_to"][user.lang].format(user["email"]), parse_mode="HTML")
        return

    assert message.text
    split_text = message.text.split()

    if len(split_text) != 2:
        await message.answer(texts["connect_e"][user.lang], parse_mode="HTML")
        return

    email = split_text[1]

    website_user = MiscDB.get_website_user(email)

    if not website_user:
        await message.answer(texts["connect_e"][user.lang], parse_mode="HTML")
        return

    if website_user["banned"]:
        await message.answer(texts["connect_e_banned"][user.lang], parse_mode="HTML")
        return

    if website_user["telegram"]:
        await message.answer(texts["connect_e_connected"][user.lang], parse_mode="HTML")
        return

    user["email"] = email
    MiscDB.set_website_telegram(user.id, email)
    await message.answer(texts["connect"][user.lang], parse_mode="HTML")