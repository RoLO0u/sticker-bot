import pymongo
import os

from typing import List, Dict, Union
from aiogram import Bot

from templates.funcs import random_string

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

def reg_user(user_id: str, username: str) -> str:
    if not users.count_documents({"userid": user_id}):
        users.insert_one({"userid": user_id, "packs": [], "username": username, "language": "en", \
            "additional_info": {"emoji": None, "name": None, "title": None}})
    user_info = users.find_one({"userid": user_id})
    return user_info["language"]

def create_pack(user_id: str, pack_name: str, title: str) -> None:
    packs.insert_one({"packid": pack_name, "title": title, "adm": user_id, "members": [user_id], "status": "making",
        "password": random_string()})
    # getting user packs and append one
    user_packs = users.find_one({"userid": user_id})["packs"] + [pack_name]
    users.update_one({"userid": user_id}, {"$set": {"packs": user_packs}})

def add_user(user_id: str, packid: str) -> None:

    pack = get_pack(packid)
    pack["members"].append(user_id)

    user_packs = get_user_packs_id(user_id)
    user_packs.append(packid)

    users.update_one({"userid": user_id}, {"$set": {"packs": user_packs}})
    packs.update_one({"packid": packid}, {"$set": {"members": pack["members"]}})

def in_pack(user_id: str, pack_id: str) -> bool:
    if user_id in get_pack(pack_id)["members"]:
        return True
    return False

def get_user_by_uname(username: str) -> Union[None, Dict]:
    if user := users.find_one({"username": username}):
        return user
    return

def get_all_packs() -> List[dict]:
    return [pack for pack in packs.find()]

def get_choosen_pack(user_id: str) -> Dict[str, Union[list, str]]:
    return get_pack(get_additional_info(user_id)["name"])

def get_pack_pass(password: str) -> Union[None, dict]:
    by_id = packs.find_one({"packid": password[:10]})
    by_pass = packs.find_one({"password": password[10:]})
    if by_id is by_pass is None:
        return
    elif by_id == by_pass:
        return by_pass

def get_pack(pack_name: str) -> Dict[str, Union[list, str]]:
    return packs.find_one({"packid": pack_name})

def get_packs_by_ids(ids: List[str], bot: Bot) -> List[dict]:
    # TODO think: write titles in database or get from telegram
    return [packs.find_one({packid["packid"]: bot.get_sticker_set(packid).title}) for packid in ids]

def get_packs_name() -> List[str]:
    return [pack["packid"] for pack in get_all_packs()]

def get_user_packs(user_id: str) -> List[Dict[str, str]]:
    """:param user_id: id of user"""
    return [{packid : get_pack_title(packid)} for packid in get_user_packs_id(user_id)]

def get_user_packs_id(user_id: str) -> List[str]:
    return users.find_one({"userid": user_id})["packs"]

def get_user_lang(user_id: str) -> str:
    return users.find_one({"userid": user_id})["language"]

def get_pack_title(pack_name: str) -> str:
    return packs.find_one({"packid": pack_name})["title"]

def get_additional_info(user_id: str) -> Dict[str, Union[None, str]]:
    return users.find_one({"userid": user_id})["additional_info"]

def delete_pack(user_id: str, pack_name: str|None = None) -> None:
    """:param pack_name: if None use users additional info as pack_name"""
    if pack_name is None:
        pack_name = get_additional_info(user_id)["name"]
    packs.delete_one({"packid": pack_name})
    # getting user packs and removing empty one
    user_packs: list = users.find_one({"userid": user_id})["packs"]
    user_packs.remove(pack_name)
    users.update_one({"userid": user_id}, {"$set": {"packs": user_packs}})

def remove_user_from_pack(user_id: str, pack_id: str) -> None:

    members = get_pack(pack_id)["members"]
    members.remove(user_id)

    user_packs = get_user_packs_id(user_id)
    user_packs.remove(pack_id)
    
    packs.update_one({"packid": pack_id}, {"$set": {"members": members}})
    users.update_one({"userid": user_id}, {"$set": {"packs": user_packs}})