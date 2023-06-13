import pymongo
import os

from typing import List, Dict, Union

from templates.funcs import random_string
from templates.Exceptions import NotFoundException

# Configuring mongodb

MONGO_URL = os.getenv("MONGO_URL")

db_client = pymongo.MongoClient(MONGO_URL)

db = db_client["usersinfo"]

users = db["users"]
packs = db["packs"]

# ---
# test funcs

def insert_dict() -> None:
    tets = db_client["tets"]
    test = tets["test"]
    test.insert_one({"Some dict": {"Hi": "World"}})
    
# ---

class Pack:
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.pack = self.get(name)
    
    @staticmethod
    def get(name: str) -> dict:
        pack = packs.find_one({"packid": name})
        if pack is None:
            raise NotFoundException(object="pack")
        return pack

    def change_status(self, change_to: str) -> None:
        packs.update_one({"packid": self.name}, {"$set": {"status": change_to}})
    
    def change_stickers(self, change_to: str) -> None:
        packs.update_one({"packid": self.name}, {"$set": {"stickers": change_to}})
    
    def include(self, user_id) -> bool:
        if user_id in self.pack["members"]:
            return True
        return False
    
    def add_user(self, user_id: str) -> None:
        self.pack['members'].append(user_id)

        user = User(user_id)
        user_packs = user.get_packs_id()
        user_packs.append(self.name)

        users.update_one({"userid": user_id}, {"$set": {"packs": user_packs}})
        packs.update_one({"packid": self.name}, {"$set": {"members": self.pack["members"]}})
        
    def get_title(self) -> str:
        title = self.pack["title"]
        if not isinstance(title, str):
            raise TypeError
        return title
    
    @staticmethod
    def get_pass(password) -> Union[None, dict]:
        by_id = packs.find_one({"packid": password[:10]})
        by_pass = packs.find_one({"password": password[10:]})
        if by_id == by_pass:
            return by_pass
    
class User:
    
    def __init__(self, user_id: str) -> None:
        self.id = user_id
        self.user = self.get(user_id)
    
    @staticmethod
    def get(user_id: str) -> dict:
        user_info = users.find_one({"userid": user_id})
        if user_info is None:
            raise NotFoundException
        return user_info
    
    def create(self, name: str, title: str) -> None:
        packs.insert_one({"packid": name, "title": title, "adm": self.id, "members": [self.id], "status": "making",
        "password": random_string()})
        # getting user packs and append one
        user_packs = User.get(self.id)["packs"] + [name]
        users.update_one({"userid": self.id}, {"$set": {"packs": user_packs}})
    
    def change(self, parameter: str, change_to: str | None) -> None:
        users.update_one({"userid": self.id}, {"$set": {f"{parameter}": change_to}})
    
    def change_lang(self, change_to: str) -> None:
        self.change("language", change_to)
    
    def change_emoji(self, change_to: str | None) -> None:
        self.change("additional_info.emoji", change_to)

    def change_name(self, change_to: str | None) -> None:
        self.change("additional_info.name", change_to)

    def change_title(self, change_to: str | None) -> None:
        self.change("additional_info.title", change_to)
        
    @staticmethod
    def register(user_id: str, username: str) -> str:
        if not User.is_exist(user_id):
            users.insert_one({"userid": user_id, "packs": [], "username": username, "language": "en", \
                "additional_info": {"emoji": None, "name": None, "title": None}})
        user_info = users.find_one({"userid": user_id})
        assert user_info is not None
        return user_info["language"]
    
    @staticmethod
    def get_by_username(username: str) -> Union[None, dict]:
        if user := users.find_one({"username": username}):
            return user
        return
    
    @staticmethod
    def is_exist(user_id: str) -> bool:
        return bool(users.count_documents({"userid": user_id}))

    def get_chosen(self) -> Dict[str, Union[list, str]]:
        chosen_pack = self.get_additional_info()["name"]
        assert chosen_pack is not None
        return Pack.get(chosen_pack)
    
    def get_packs(self) -> List[Dict[str, str]]:
        return [{packid : Pack(packid).get_title()} for packid in self.get_packs_id()]

    def get_packs_id(self) -> List[str]:
        return self.user["packs"]
    
    def get_user_lang(self) -> str:
        return self.user["language"]
    
    def get_additional_info(self) -> Dict[str, Union[None, str]]:
        return self.user["additional_info"]

    def delete_pack(self) -> None:
        """:param pack_name: if None use users additional info as pack_name"""
        pack_name = self.get_additional_info()["name"]
        # getting user packs and removing empty one
        # TODO use update_many to delete pack from many users
        user_packs: list = self.user["packs"]
        user_packs.remove(pack_name)
        packs.delete_one({"packid": pack_name})
        users.update_one({"userid": self.id}, {"$set": {"packs": user_packs}})
        
    def remove_user_from_pack(self, pack_id: str) -> None:

        members = Pack.get(pack_id)["members"]
        if isinstance(members, list):
            members.remove(self.id)

        user_packs = self.get_packs_id()
        user_packs.remove(pack_id)
        
        packs.update_one({"packid": pack_id}, {"$set": {"members": members}})
        users.update_one({"userid": self.id}, {"$set": {"packs": user_packs}})

def get_user_by_uname(username: str) -> Union[None, Dict]:
    if user := users.find_one({"username": username}):
        return user

def get_all_packs() -> List[dict]:
    return [pack for pack in packs.find()]

def get_packs_name() -> List[str]:
    return [pack["packid"] for pack in get_all_packs()]