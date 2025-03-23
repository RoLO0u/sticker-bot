import pymongo
import os

from typing import List, Dict, Union, Optional

from templates.funcs import random_string
from templates.Exceptions import NotFoundException
from templates.database import baseDB

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

class Pack(baseDB.Pack):
        
    @classmethod
    def _get(cls, name: str) -> dict:
        pack = packs.find_one({"packid": name})
        if pack is None:
            raise NotFoundException(object=cls.__name__)
        return pack
        
    def change(self, parameter: str, change_to: str | None) -> None:
        packs.update_one({"packid": self.name}, {"$set": {parameter: change_to}})
    
    @staticmethod
    def get_pass(password: str) -> Optional[dict]:
        by_id = packs.find_one({"packid": password[:10]})
        by_pass = packs.find_one({"password": password[10:]})
        if by_id == by_pass:
            return by_pass
        
    def add_user(self, user_id: str) -> None:
        self.pack['members'].append(user_id)

        user = User(user_id)
        user_packs = user["packs"]
        user_packs.append(self.name)

        user.change("packs", user_packs)
        self.change("members", self.pack["members"])
        
class User(baseDB.User):
    
    @classmethod
    def _get(cls, user_id: str) -> dict:
        user = users.find_one({"userid": user_id})
        if user is None:
            raise NotFoundException(object=cls.__name__)
        return user
    
    def create(self, name: str, title: str) -> None:
        packs.insert_one({"packid": name, "title": title, "adm": self.id, "members": [self.id], "status": "making",
        "password": random_string()})
        # getting user packs and append one
        user_packs = self.user["packs"] + [name]
        users.update_one({"userid": self.id}, {"$set": {"packs": user_packs}})
    
    def change(self, parameter: str, change_to: str | list | None) -> None:
        users.update_one({"userid": self.id}, {"$set": {parameter: change_to}})
        
    @staticmethod
    def register(user_id: str, username: Optional[str], first_name: str) -> str:
        if not User.is_exist(user_id):
            users.insert_one({"userid": user_id, "packs": [], "username": username, "language": "en", \
                "emoji": None, "name": None, "title": None, "stickers": [], "emojis": [], "sticker": None, \
                "image": None, "first_name": first_name})
        user_info = users.find_one({"userid": user_id})
        assert user_info
        if user_info["username"] != username:
            User(user_id)["username"] = username
        return user_info["language"]
    
    @staticmethod
    def get_by_username(username: str) -> Optional[dict]:
        if user := users.find_one({"username": username}):
            return user
    
    @staticmethod
    def is_exist(user_id: str) -> bool:
        return bool(users.count_documents(filter={"userid": user_id}))

    def get_chosen(self) -> Pack:
        chosen_pack = self.user["name"]
        assert chosen_pack
        return Pack(chosen_pack)
    
    def get_packs(self) -> List[Dict[str, str]]:
        return [{packid : Pack(packid)["title"]} for packid in self["packs"]]

    def delete_pack(self, pack_name: Optional[str] = None) -> None:
        if pack_name is None:
            pack_name = self.user["name"]
            assert pack_name
        pack = Pack(pack_name)
        for pack_member in pack.pack["members"]:
            member_packs: list = User(pack_member).user["packs"]
            member_packs.remove(pack.name)
            users.update_one({"userid": pack_member}, {"$set": {"packs": member_packs}})
        packs.delete_one({"packid": pack.name})
        
    def remove_from_pack(self, pack_id: str) -> None:
        members = Pack._get(pack_id)["members"]
        if isinstance(members, list):
            members.remove(self.id)

        user_packs = self["packs"]
        user_packs.remove(pack_id)
        
        packs.update_one({"packid": pack_id}, {"$set": {"members": members}})
        users.update_one({"userid": self.id}, {"$set": {"packs": user_packs}})

class MiscDB(baseDB.MiscDB):
    
    @staticmethod
    def get_all_packs() -> List[dict]:
        return [pack for pack in packs.find()]