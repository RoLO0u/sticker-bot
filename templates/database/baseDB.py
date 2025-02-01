from abc import ABC, abstractmethod
from typing import Optional, Union, Dict, Any, List, Type

from templates.database import baseDB

class Object(ABC):
    
    @classmethod
    @abstractmethod
    def get(cls, name: str) -> Dict[str, Any]:
        ...
    
    @abstractmethod
    def change(self, parameter: str, change_to: Optional[Any]) -> None:
        ...
    
class Pack(Object):
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.pack = self.get(name)
        
    def change_status(self, change_to: str) -> None:
        self.change("status", change_to)
        
    def change_stickers(self, change_to: str) -> None:
        self.change("stickers", change_to)
        
    def include(self, user_id) -> bool:
        if user_id in self.pack["members"]:
            return True
        return False
    
    @abstractmethod
    def add_user(self, user_id: str) -> None:
        ...
        
    def get_title(self) -> str:
        title = self.pack["title"]
        if not isinstance(title, str):
            raise TypeError
        return title
    
    @staticmethod
    @abstractmethod
    def get_pass(password) -> Union[None, dict]:
        ...
    
class User(Object):
    
    def __init__(self, user_id: str) -> None:
        self.id = user_id
        self.user = self.get(user_id)

    def __getitem__(self, item: str):
        return self.user[item]
    
    @abstractmethod
    def create(self, name: str, title: str) -> None:
        """Create pack in database

        Args:
            name (str): name (packid) for the pack
            title (str): title (caption) for the pack, which will be seen by user
        """
        ...
    
    def change_lang(self, change_to: str) -> None:
        self.change("language", change_to)
    
    def change_emoji(self, change_to: Optional[str]) -> None:
        self.change("emoji", change_to)

    def change_name(self, change_to: Optional[str]) -> None:
        self.change("name", change_to)

    def change_title(self, change_to: Optional[str]) -> None:
        self.change("title", change_to)
        
    def change_username(self, change_to: Optional[str]) -> None:
        self.change("username", change_to)
        
    @staticmethod
    @abstractmethod
    def register(user_id: str, username: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def get_by_username(username: str) -> Union[None, dict]:
        ...
    
    @staticmethod
    @abstractmethod
    def is_exist(user_id: str) -> bool:
        ...

    @abstractmethod
    def get_chosen(self) -> Dict[str, Union[list, str]]:
        """Gets chosen pack

        Returns:
            Dict[str, Union[list, str]]: Pack instance user had chose
        """
        ...
    
    @abstractmethod
    def get_packs(self) -> List[Dict[str, str]]:
        ...

    def get_packs_id(self) -> List[str]:
        return self.user["packs"]
    
    def get_user_lang(self) -> str:
        return self.user["language"]

    @abstractmethod
    def delete_pack(self, pack_name: Optional[str] = None) -> None:
        ...
        
    @abstractmethod
    def remove_user_from_pack(self, pack_id: str) -> None:
        ...

class MiscDB(ABC):

    @staticmethod
    @abstractmethod
    def get_all_packs() -> List[dict]:
        ...

    @classmethod
    def get_packs_name(cls) -> List[str]:
        return [pack["packid"] for pack in cls.get_all_packs()]