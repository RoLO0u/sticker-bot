from typing import Any, Dict, List, Optional, Union
from psycopg2._psycopg import cursor
from psycopg2.sql import SQL, Identifier
import os

from templates.database import baseDB
from templates.Exceptions import NotFoundException
from templates.funcs import random_string, convert_pack_sql, convert_user_sql
from templates.database.fsm.postgres import PostgreStorage, read_sql

kwargs = {"database": os.getenv("PGDATABASE"), \
        "host": os.getenv("PGHOST"), \
        "port": os.getenv("PGPORT"), \
        "user": os.getenv("PGUSER"), \
        "password": os.getenv("PGPASSWORD")}

if os.getenv("SSLMODE") == "require":
    kwargs["sslmode"] = os.getenv("SSLMODE")
    kwargs["sslrootcert"] = os.getenv("SSLROOTCERT")

assert all(kwargs.values()) # ensures all values are not none
conn = PostgreStorage.connect(**kwargs) # type: ignore

def default(func):
    """Default decorator, which gives cursor and more security for the database
    defines and sends user_id
    
    As pylance can't understand, that this decorator passes _cur,
    decorated function should set default value
    """
    def wrapper(*args, **kwargs):
        with conn.cursor() as cur:
            to_return = func(*args, _cur=cur, **kwargs)
            conn.commit()
            return to_return
    return wrapper

class Pack(baseDB.Pack):
    
    @classmethod
    @default
    def _get(cls, name: str, _cur: Optional[cursor] = None) -> Dict[str, Any]:
        assert _cur
        _cur.execute(read_sql("get/pack.sql"), (name,))
        result = _cur.fetchone()
        if result is None:
            raise NotFoundException(object=name)
        return convert_pack_sql(result)
    
    @classmethod
    @default
    def _get_by_pass(cls, password: str, _cur: Optional[cursor] = None) -> Dict[str, Any]:
        assert _cur
        _cur.execute(read_sql("get/pack_by_password.sql"), (password,))
        result = _cur.fetchone()
        if result is None:
            raise NotFoundException(object=password)
        return convert_pack_sql(result)
    
    def add_user(self, user_id: str) -> None:
        self.pack['members'].append(user_id)

        user = User(user_id)
        user_packs = user["packs"]
        user_packs.append(self.name)

        user.change("packs", user_packs)
        self.change("members", self.pack["members"])
    
    @default
    def change(self, parameter: str,
            change_to: str | list | None, 
            _cur: Optional[cursor] = None) -> None:
        assert _cur
        _cur.execute(
            SQL(read_sql("change/pack.sql")).format(Identifier(parameter)), 
            (change_to, self.name))
    
    @staticmethod
    @default
    def get_pass(password: str, _cur: Optional[cursor] = None) -> Optional[Dict]:
        assert _cur
        by_id = Pack._get(password[:10])        
        by_pass = Pack._get_by_pass(password[10:])
        if (by_id == by_pass):
            return by_pass
        
class User(baseDB.User):
        
    @classmethod
    @default
    def _get(cls, user_id: str, _cur: Optional[cursor] = None) -> Dict[str, Any]:
        assert _cur
        _cur.execute(read_sql("get/user.sql"), (user_id,))
        result = _cur.fetchone()
        if result is None:
            raise NotFoundException(object=cls.__name__)
        return convert_user_sql(result)
        
    @default
    def create(self, name: str, title: str, _cur: Optional[cursor] = None) -> None:
        assert _cur
        self.user["packs"] += [name]
        _cur.execute(read_sql("create/pack.sql"),
            (name, title, self.id, [self.id], "making", random_string(), # creating pack
             self.user["packs"], self.id)) # updating user packs list
        
    @default
    def change(self, parameter: str,
            change_to: str | None | list, 
            _cur: Optional[cursor] = None) -> None:
        assert _cur
        _cur.execute(
            SQL(read_sql("change/user.sql")).format(Identifier(parameter)), 
            (change_to, self.id))
        
    @staticmethod
    @default
    def register(user_id: str, username: Optional[str], first_name: str, _cur: Optional[cursor] = None) -> str:
        assert _cur
        if not User.is_exist(user_id):
            _cur.execute(read_sql("create/user.sql"), (user_id, username, first_name))
        _cur.execute(read_sql("get/user.sql"), (user_id,))
        user_info = _cur.fetchone()
        assert user_info
        if user_info[2] != username:
            User(user_id)["username"] = username
        return user_info[3]
            
    @staticmethod
    @default
    def get_by_username(username: str, _cur: Optional[cursor] = None) -> Optional[dict]:
        assert _cur
        _cur.execute(read_sql("get/user_by_name.sql"), (username,))
        if user := _cur.fetchone():
            return convert_user_sql(user)
    
    @staticmethod
    @default
    def is_exist(user_id: str, _cur: Optional[cursor] = None) -> bool:
        assert _cur
        _cur.execute(read_sql("get/user.sql"), (user_id,))
        return bool(_cur.fetchone())
    
    def get_chosen(self) -> Optional[Pack]:
        chosen_pack: Optional[str] = self.user["name"]
        if chosen_pack:
            return Pack(chosen_pack)
    
    def get_packs(self) -> List[Dict[str, str]]:
        return [{packid : Pack(packid)["title"]} for packid in self["packs"]]
    
    @default
    def delete_pack(self, pack_name: Optional[str] = None, _cur: Optional[cursor] = None) -> None:
        assert _cur
        if pack_name is None:
            pack_name = self["name"]
            assert pack_name
        pack = Pack(pack_name)
        for pack_member in pack.pack["members"]:
            user = User(pack_member)
            member_packs: list = user.user["packs"]
            member_packs.remove(pack.name)
            user.change("packs", member_packs)
        _cur.execute(read_sql("delete/pack.sql"), (pack.name,))

    @default
    def remove_from_pack(self, pack_id: str, _cur: Optional[cursor] = None) -> None:
        assert _cur
        members = Pack._get(pack_id)["members"]
        if isinstance(members, list):
            members.remove(self.id)

        user_packs = self["packs"]
        user_packs.remove(pack_id)
        
        Pack(pack_id).change("members", members)
        User(self.id).change("packs", user_packs)

class MiscDB(baseDB.MiscDB):
    
    @staticmethod
    @default
    def create_tables(_cur: Optional[cursor] = None) -> None:
        assert _cur
        _cur.execute(read_sql("create/tables.sql"))
            
    @staticmethod
    @default
    def get_all_packs(_cur: Optional[cursor] = None) -> List[dict]:
        assert _cur
        _cur.execute(read_sql("get/all_packs.sql"))
        return [convert_pack_sql(pack) for pack in _cur.fetchall()]