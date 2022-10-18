import random
import string
from emoji import EMOJI_DATA
from PIL import Image
from io import BytesIO
from templates.database import get_packs_title

def is_emoji(chars: str) -> bool:
    return all([char in EMOJI_DATA for char in chars])

def resize_image(image: BytesIO, user_id: str):
    # with open(f"photos/{user_id}/image.png", 'wb') as new_file:
    #     new_file.write(image)
    # image = Image.open(f"photos/{user_id}/image.png")
    # print(type(image))
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
    return bio

async def pack_availability(func, exception, caption: str) -> bool:
    try:
        await func(caption)
    except exception:
        return False
    else:
        return True

def random_string(L: int = 10) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=L))

def user_packs(packs: dict, user_packs_name: list) -> list:
    return [[get_packs_title(pack), pack] for pack in user_packs_name]