from typing import BinaryIO
from PIL import Image
from io import BytesIO

from aiogram import Bot
from aiogram.types import BufferedInputFile, InputFile, PhotoSize

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

async def create_input_file(bot: Bot, photo: str) -> InputFile:
    file_info = await bot.get_file(photo)
    assert file_info.file_path
    raw_file = await bot.download_file(file_info.file_path)
    assert raw_file
    return resize_image(raw_file)