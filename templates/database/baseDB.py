from abc import ABC, abstractmethod
from typing import Optional, Union, Dict, Any, List

from templates.database import baseDB

class Object(ABC):
    
    @classmethod
    @abstractmethod
    def _get(cls, name: str) -> Dict[str, Any]:
        ...
    
    @abstractmethod
    def change(self, parameter: str, change_to: Optional[Any]) -> None:
        ...
    
class Pack(Object):
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.pack = self._get(name)

    def __getitem__(self, item: str) -> Any:
        return self.pack[item]
    
    def __setitem__(self, index: str, value: Any) -> None:
        self.pack[index] = value
        self.change(index, value)
        
    def includes(self, user_id: str) -> bool:
        if user_id in self.pack["members"]:
            return True
        return False
    
    @abstractmethod
    def add_user(self, user_id: str) -> None:
        ...
        
    @staticmethod
    @abstractmethod
    def get_pass(password) -> Union[None, dict]:
        ...
    
class User(Object):
    
    def __init__(self, user_id: str) -> None:
        self.id = user_id
        self.user = self._get(user_id)
        self.lang = self.user["language"]

    def __getitem__(self, item: str) -> Any:
        return self.user[item]
    
    def __setitem__(self, index: str, value: Any) -> None:
        self.user[index] = value
        self.change(index, value)
    
    @abstractmethod
    def create(self, name: str, title: str) -> None:
        """Create pack in database

        Args:
            name (str): name (packid) for the pack
            title (str): title (caption) for the pack, which will be seen by user
        """
        ...
        
    @staticmethod
    @abstractmethod
    def register(user_id: str, username: Optional[str], first_name: str) -> str:
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
    def get_chosen(self) -> Optional[Pack]:
        """Gets chosen pack

        Returns:
            Pack instance user had chosen
        """
        ...
    
    @abstractmethod
    def get_packs(self) -> List[Dict[str, str]]:
        ...

    @abstractmethod
    def delete_pack(self, pack_name: Optional[str] = None) -> None:
        ...
        
    @abstractmethod
    def remove_from_pack(self, pack_id: str) -> None:
        ...

class MiscDB(ABC):

    @staticmethod
    @abstractmethod
    def get_all_packs() -> List[dict]:
        ...

    @classmethod
    def get_packs_name(cls) -> List[str]:
        return [pack["packid"] for pack in cls.get_all_packs()]