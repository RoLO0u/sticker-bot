from typing import BinaryIO
from PIL import Image
from io import BytesIO
from aiogram.types import BufferedInputFile
from aiogram.types import InputFile

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

async def create_InputFile(get_file, photo, download_file) -> InputFile:
    raw_file = await get_file(photo[len(photo)-1].file_id)
    photo = resize_image(await download_file(raw_file.file_path))

    return photo
