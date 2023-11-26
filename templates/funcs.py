import random
import string

from typing import BinaryIO, Tuple, Optional, Type, Dict, Any
from emoji import EMOJI_DATA
from PIL import Image
from io import BytesIO

from templates.database import baseDB
from templates.const import WATERMARK

from aiogram.types import BufferedInputFile, InputFile, StickerSet
from aiogram.exceptions import TelegramBadRequest

def is_emoji(chars: str) -> bool:
    return all([char in EMOJI_DATA for char in chars])

def resize_image(imageIO: BinaryIO) -> InputFile:
    image = Image.open(imageIO)
    base = 512
    min_size = min(image.size)
    max_size = max(image.size)
    percent = base / max_size
    resize_to = (base, int(min_size * percent)) if max_size == image.size[0] else (int(min_size * percent), base)
    image = image.resize(resize_to, Image.Resampling.LANCZOS)
    bio = BytesIO()
    bio.name = 'last_image.png'
    image.save(bio, 'PNG')
    bio.seek(0)
    raw = bio.read1()
    image = BufferedInputFile(file=raw, filename="last_image.png")
    return image

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
        if not await pack_exists(get_sticker_set, pname+WATERMARK):
            to_pop.append(pname)
    for pname in to_pop:
        user.delete_pack(pname)

async def get_create_add_info(user_id: str, User: Type[baseDB.User], get_file, photo, download_file) -> Tuple[str, str, Optional[str], InputFile, Optional[str]]:

    user = User(user_id)
    additional_info = user.get_additional_info()
    pack_name = additional_info["name"]
    assert pack_name
    pack_name_plus = pack_name + WATERMARK
    title = additional_info["title"]
    raw_file = await get_file(photo[len(photo)-1].file_id)
    photo = resize_image(await download_file(raw_file.file_path))
    emoji = additional_info["emoji"]

    return pack_name, pack_name_plus, title, photo, emoji

async def have_stickers(packid: str, get_sticker_set) -> bool:
    sticker_set: StickerSet = await get_sticker_set(packid+WATERMARK)
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
            "additional_info": data[4]
            }