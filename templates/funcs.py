import json
import random
import string
from emoji import EMOJI_DATA
from PIL import Image
from io import BytesIO

def is_emoji(captions: str) -> bool:
    return all([caption in EMOJI_DATA for caption in captions])

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
        db["users"][user_id] = {"username": username, "packs": [], "language": "en", "status": None, "additional_info": None}
        db["username_to_id"][username] = user_id
    return db

def resize_image(image):
    with open("last_image.png", 'wb') as new_file:
        new_file.write(image)
    image = Image.open("last_image.png")
    image.thumbnail((512, 512))
    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')
    bio.seek(0)
    return bio

def pack_availability(func, exception, caption: str) -> bool:
    try:
        func(caption)
    except exception:
        return False
    else:
        return True

def random_string(L: int = 10) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=L))

PM = lambda message: message.chat.type == "private"