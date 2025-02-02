"""
This module has mongo storage for finite-state machine
    based on `motor <https://github.com/mongodb/motor>`_ driver
"""

from typing import Any, Union, Dict, Optional, List, Tuple
from aiogram.fsm.storage.base import (
    DEFAULT_DESTINY,
    BaseEventIsolation,
    BaseStorage,
    StateType,
    StorageKey,
)

try:
    import pymongo
    import pymongo.errors
    import motor
    from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
except ModuleNotFoundError as e:
    import warnings
    warnings.warn("Install motor with `pip install motor`")
    raise e

STATE = 'aiogram_state'
DATA = 'aiogram_data'
BUCKET = 'aiogram_bucket'
COLLECTIONS = (STATE, DATA, BUCKET)

class MongoStorage(BaseStorage):
    """
    Mongo-based storage for FSM.
    Usage:
    .. code-block:: python3
        storage = MongoStorage(host='localhost', port=27017, db_name='aiogram_fsm')
        dp = Dispatcher(bot, storage=storage)
    And need to close Mongo client connections when shutdown
    .. code-block:: python3
        await dp.storage.close()
        await dp.storage.wait_closed()
    """

    def __init__(self, host='localhost', port=27017, db_name='aiogram_fsm', uri=None,
                 username=None, password=None, index=True, **kwargs):
        self._host = host
        self._port = port
        self._db_name: str = db_name
        self._uri = uri
        self._username = username
        self._password = password
        self._kwargs = kwargs  # custom client options like SSL configuration, etc.

        self._mongo = Optional[AsyncIOMotorClient]
        self._db = Optional[AsyncIOMotorDatabase]
        

        self._index = index

    async def get_client(self) -> AsyncIOMotorClient: # type: ignore
        if isinstance(self._mongo, AsyncIOMotorClient):
            return self._mongo

        if self._uri:
            try:
                self._mongo = AsyncIOMotorClient(self._uri, **self._kwargs)
            except pymongo.errors.ConfigurationError as e:
                if "query() got an unexpected keyword argument 'lifetime'" in e.args[0]:
                    import logging
                    logger = logging.getLogger("aiogram")
                    logger.warning("Run `pip install dnspython==1.16.0` in order to fix ConfigurationError. More information: https://github.com/mongodb/mongo-python-driver/pull/423#issuecomment-528998245")
                raise e
            return self._mongo

        uri = 'mongodb://'

        # set username + password
        if self._username and self._password:
            uri += f'{self._username}:{self._password}@'

        # set host and port (optional)
        uri += f'{self._host}:{self._port}' if self._host else f'localhost:{self._port}'

        # define and return client
        self._mongo = AsyncIOMotorClient(uri)
        return self._mongo

    @staticmethod
    def resolve_state(value):
        from aiogram.fsm.state import State
        
        if value is None:
            return

        if isinstance(value, str):
            return value

        if isinstance(value, State):
            return value.state

        return str(value)

    async def get_db(self) -> AsyncIOMotorDatabase: # type: ignore
        """
        Get Mongo db
        This property is awaitable.
        """
        if isinstance(self._db, AsyncIOMotorDatabase):
            return self._db

        mongo = await self.get_client()
        self._db = mongo.get_database(self._db_name)

        if self._index:
            await self.apply_index(self._db)
        return self._db # type: ignore
    
    @classmethod
    def check_address(cls, *,
                      chat: Union[str, int, None] = None,
                      user: Union[str, int, None] = None,
                      ) -> Tuple[Union[str, int], Union[str, int]]:
        """
        In all storage's methods chat or user is always required.
        If one of them is not provided, you have to set missing value based on the provided one.
        This method performs the check described above.
        :param chat: chat_id
        :param user: user_id
        :return:
        """
        if chat is None and user is None:
            raise ValueError('`user` or `chat` parameter is required but no one is provided!')

        if user is None:
            user = chat

        elif chat is None:
            chat = user

        # VS Code:
        # Pylance thinks chat or user can be None
        return chat, user # type: ignore

    @staticmethod
    async def apply_index(db):
        for collection in COLLECTIONS:
            await db[collection].create_index(keys=[('chat', 1), ('user', 1)],
                                              name="chat_user_idx", unique=True, background=True)

    async def close(self):
        if self._mongo:
            self._mongo.close() # type: ignore

    async def wait_closed(self):
        return True

    async def set_state(self, *,
                        key: StorageKey,
                        state: StateType = None):
        chat, user = self.check_address(chat=key.chat_id, user=key.user_id)
        db = await self.get_db()

        if state is None:
            await db[STATE].delete_one(filter={'chat': chat, 'user': user})
        else:
            await db[STATE].update_one(
                filter={'chat': chat, 'user': user},
                update={'$set': {'state': self.resolve_state(state)}},
                upsert=True,
            )

    async def get_state(self,
        key: StorageKey,) -> Optional[str]:
        chat, user = self.check_address(chat=key.chat_id, user=key.user_id)
        db = await self.get_db()
        result = await db[STATE].find_one(filter={'chat': chat, 'user': user})

        return result.get('state') if result else self.resolve_state(key.destiny)

    async def set_data(self, key: StorageKey, data: Dict[str, Any]):
        chat, user = self.check_address(chat=key.chat_id, user=key.user_id)
        db = await self.get_db()
        if not data:
            await db[DATA].delete_one(filter={'chat': chat, 'user': user})
        else:
            await db[DATA].update_one(filter={'chat': chat, 'user': user},
                                      update={'$set': {'data': data}}, upsert=True)

    async def get_data(self, key: StorageKey) -> Dict:
        chat, user = self.check_address(chat=key.chat_id, user=key.user_id)
        db = await self.get_db()
        result = await db[DATA].find_one(filter={'chat': chat, 'user': user})

        return result.get('data') if result else dict()

    def has_bucket(self):
        return True

    async def get_bucket(self, *, chat: Union[str, int, None] = None, user: Union[str, int, None] = None,
                         default: Optional[dict] = None) -> Dict:
        chat, user = self.check_address(chat=chat, user=user)
        db = await self.get_db()
        result = await db[BUCKET].find_one(filter={'chat': chat, 'user': user})
        return result.get('bucket') if result else default or {}

    async def set_bucket(self, *, chat: Union[str, int, None] = None, user: Union[str, int, None] = None,
                         bucket: Optional[Dict] = None):
        chat, user = self.check_address(chat=chat, user=user)
        db = await self.get_db()

        await db[BUCKET].update_one(filter={'chat': chat, 'user': user},
                                    update={'$set': {'bucket': bucket}}, upsert=True)

    async def update_bucket(self, *, chat: Union[str, int, None] = None,
                            user: Union[str, int, None] = None,
                            bucket: Optional[Dict] = None, **kwargs):
        if bucket is None:
            bucket = {}
        temp_bucket = await self.get_bucket(chat=chat, user=user)
        temp_bucket.update(bucket, **kwargs)
        await self.set_bucket(chat=chat, user=user, bucket=temp_bucket)

    async def reset_all(self, full=True):
        """
        Reset states in DB
        :param full: clean DB or clean only states
        :return:
        """
        db = await self.get_db()

        await db[STATE].drop()

        if full:
            await db[DATA].drop()
            await db[BUCKET].drop()

    async def get_states_list(self) -> List[Tuple[int, int]]:
        """
        Get list of all stored chat's and user's
        :return: list of tuples where first element is chat id and second is user id
        """
        db = await self.get_db()
        items = await db[STATE].find().to_list(length=None) # type: ignore
        return [(int(item['chat']), int(item['user'])) for item in items]