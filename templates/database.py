import pymongo
import os

# Configuring mongodb

MONGO_URL = os.getenv("MONGO_URL")

db_client = pymongo.MongoClient(MONGO_URL)

db = db_client["usersinfo"]

users = db["users"]
packs = db["packs"]

# ---
# test funcs

def get_user_info(user_id: str) -> dict:
    return users.find_one({"userid": user_id})

def insert_dict() -> None:
    tets = db_client["tets"]
    test = tets["test"]
    test.insert_one({"Some dict": {"Hi": "World"}})
# ---

def change_status(user_id: str, change_to: str) -> None:
    users.update_one({"userid": user_id}, {"$set": {"status": change_to}})

def change_pack_status(pack_name: str, change_to: str) -> None:
    packs.update_one({"packid": pack_name}, {"$set": {"status": change_to}})

def change_lang(user_id: str, change_to: str) -> None:
    users.update_one({"userid": user_id}, {"$set": {"language": change_to}})

def change_emoji(user_id: str, change_to: str | None) -> None:
    users.update_one({"userid": user_id}, {"$set": {"additional_info.emoji": change_to}})

def change_name(user_id: str, change_to: str | None) -> None:
    users.update_one({"userid": user_id}, {"$set": {"additional_info.name": change_to}})

def change_title(user_id: str, change_to: str | None) -> None:
    users.update_one({"userid": user_id}, {"$set": {"additional_info.title": change_to}})

def change_pack_stickers(pack_name: str, change_to: list) -> None:
    packs.update_one({"packid": pack_name}, {"$set": {"stickers": change_to}})

def reg_user(user_id: str, username: str) -> tuple:
    if not users.count_documents({"userid": user_id}):
        users.insert_one({"userid": user_id, "username": username, "packs": [], "language": "en", "status": "start", \
            "additional_info": {"emoji": None, "name": None, "title": None}})
    user_info = users.find_one({"userid": user_id})
    return user_info["language"], user_info["status"]

def create_pack(user_id: str, pack_name: str, title: str) -> None:
    packs.insert_one({"packid": pack_name, "title": title, "adm": user_id, "members": [user_id], "stickers": [], "status": "making"})
    # getting user packs and append one
    user_packs = users.find_one({"userid": user_id})["packs"] + [pack_name]
    users.update_one({"userid": user_id}, {"$set": {"packs": user_packs}})

def get_all_packs() -> list:
    return [pack for pack in packs.find()]

def get_pack(pack_name: str) -> dict:
    return packs.find_one({"packid": pack_name})

def get_packs_name() -> list:
    return [pack["packid"] for pack in get_all_packs()]

def get_user_packs_name(user_id: str) -> list:
    return users.find_one({"userid": user_id})["packs"]

def get_user_lang(user_id: str) -> str:
    return users.find_one({"userid": user_id})["language"]

def get_packs_title(pack_name: str) -> str:
    return packs.find_one({"packid": pack_name})["title"]

def get_additional_info(user_id: str) -> str:
    return users.find_one({"userid": user_id})["additional_info"]

def remove_sticker_from_pack(pack_name: str, sticker_unique_id: str) -> None:
    stickers = get_pack(pack_name)["stickers"]
    stickers.remove(sticker_unique_id)
    packs.update_one({"packid": pack_name}, {"$set": {"stickers": stickers}})

def delete_pack(user_id: str, pack_name: str|None = None) -> None:
    """:param pack_name: if None use users additional info as pack_name"""
    if pack_name is None:
        pack_name = get_additional_info(user_id)["name"]
    packs.delete_one({"packid": pack_name})
    # getting user packs and removing empty one
    user_packs = users.find_one({"userid": user_id})["packs"]
    user_packs.remove(pack_name)
    users.update_one({"userid": user_id}, {"$set": {"packs": user_packs}})