import random
import string

from typing import List, Union
from emoji import EMOJI_DATA
from PIL import Image
from io import BytesIO

from templates import database
from templates.const import WATERMARK

from aiogram.types import BufferedInputFile, InputFile, StickerSet
from aiogram.exceptions import TelegramBadRequest

def is_emoji(chars: str) -> bool:
    return all([char in EMOJI_DATA for char in chars])

def resize_image(image: BytesIO) -> InputFile:
    image = Image.open(image)
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
    else:
        return True

async def delete_non_exist(get_sticker_set, user_id: str) -> None:

    to_pop = []
    for pname in database.get_user_packs_id(user_id):
        if not await pack_exists(get_sticker_set, pname+WATERMARK):
            to_pop.append(pname)
    for pname in to_pop:
        # TODO don't forget to edit when members support added
        database.delete_pack(user_id, pname)

async def get_create_add_info(user_id: str, get_file, photo, download_file) -> List[Union[str, InputFile]]:

    additional_info = database.get_additional_info(user_id)
    pack_name = additional_info["name"]
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