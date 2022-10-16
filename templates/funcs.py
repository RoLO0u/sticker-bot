import json
import random
import string
from emoji import EMOJI_DATA
from PIL import Image
from io import BytesIO

def is_emoji(chars: str) -> bool:
    return all([char in EMOJI_DATA for char in chars])

def load_db() -> dict:
    """*.json files only"""
    with open("usersinfo.json", "r", encoding="utf-8") as database:
        db = json.load(database)
    return db

def upload_db(db: dict) -> None:
    with open("usersinfo.json", "w", encoding="utf-8") as database:
        json.dump(db, database, indent=2, ensure_ascii=False)

def reg_user(user_id: str, username: str) -> dict:
    """reg user and imports db"""
    db = load_db()
    if not user_id in db["users"] and not username is None:
        db["users"][user_id] = {"username": username, "packs": [], "language": "en", "status": "start", "additional_info": None}
    return db

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
    return [[packs[pack]["title"], pack] for pack in user_packs_name]