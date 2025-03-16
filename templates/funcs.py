import random
import string

from typing import Tuple, Optional, Type, Dict, Any
from emoji import is_emoji
from templates.database import baseDB
from templates.const import WATERMARK

from aiogram.types import StickerSet
from aiogram.exceptions import TelegramBadRequest

def is_emojis(chars: str) -> list[str]:
    return [char for char in chars if is_emoji(char)]

async def pack_exists(get_sticker_set, packid: str) -> bool:
    try:
        await get_sticker_set(packid)
    except TelegramBadRequest:
        return False
    return True

async def delete_non_exist(get_sticker_set, User: Type[baseDB.User], user_id: str) -> None:

    user = User(user_id)
    to_pop = []
    for pname in user.get_packs_id():
        if not await pack_exists(get_sticker_set, pname+str(WATERMARK)):
            to_pop.append(pname)
    for pname in to_pop:
        user.delete_pack(pname)
   
async def get_create_add_info(user: baseDB.User) -> Tuple[str, str, Optional[str], Optional[str]]:

    pack_name = user["name"]
    assert pack_name
    pack_name_plus = pack_name + str(WATERMARK)
    title = user["title"]
    emoji = user["emoji"]

    return pack_name, pack_name_plus, title, emoji

async def have_stickers(packid: str, get_sticker_set) -> bool:
    sticker_set: StickerSet = await get_sticker_set(packid+str(WATERMARK))
    return not not sticker_set.stickers # It for some reason faster than bool(obj) in 2 times
    # https://stackoverflow.com/questions/25594231/why-is-not-faster-than-bool-in-python-or-speed-of-python-functions-vs-s

def random_string(L: int = 10) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=L))

def convert_pack_sql(data: Tuple[Any, ...]) -> Dict[str, Any]:
    return {
            "packid": data[0],
            "title": data[1],
            "adm": data[2],
            "members": data[3],
            "status": data[4],
            "password": data[5]
            }
    
def convert_user_sql(data: Tuple[Any, ...]) -> Dict[str, Any]:
    return {
            "userid": data[0],
            "packs": data[1],
            "username": data[2],
            "language": data[3],
            "name": data[4],
            "title": data[5],
            "emoji": data[6],
            "stickers": data[7],
            "emojis": data[8],
            "sticker": data[9],
            "image": data[10]
            }