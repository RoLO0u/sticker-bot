"""
This module has mongo storage for finite-state machine
    based on `motor <https://github.com/mongodb/motor>`_ driver
"""
from typing import Dict, Optional, Any
from aiogram import Bot
from aiogram.fsm.storage.base import (
    BaseStorage,
    StateType,
    StorageKey,
)

import json
import psycopg2
from psycopg2._psycopg import connection

STATE = 'aiogram_state'
DATA = 'aiogram_data'
BUCKET = 'aiogram_bucket'
COLLECTIONS = (STATE, DATA, BUCKET)

def read_sql(file_path: str) -> str:
    with open(f"templates/database/sql_queries/{file_path}", "r", encoding="utf-8") as raw_file:
        return raw_file.read()

class PostgreStorage(BaseStorage):

    def __init__(self, database: str, host: str, port: str,
                 user: str, password: str, index=True, **kwargs):
        self._host = host
        self._port = port
        self._db_name = database
        self._username = user
        self._password = password
        self._kwargs = kwargs  # custom client options like SSL configuration, etc.

        self._conn = self.connect(self._host, self._port, self._db_name, self._username, self._password)
        self._cur = self._conn.cursor()
        self.create_tables()
        self._index = index

        
    def create_tables(self):
        self._cur.execute(read_sql("create/tables_fsm.sql"))
        self._conn.commit()
        
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
        
    @staticmethod
    def connect(host: str, port: str, database: str, user: str, password: str) -> connection:
        with psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
                ) as conn:
            return conn
        
    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        state = self.resolve_state(state)
        user_id = str(key.user_id)
        self._cur.execute(read_sql("change/state.sql"), (user_id,state,user_id,user_id,state))
        self._conn.commit()
        
    async def get_state(self, key: StorageKey) -> Optional[str]:
        self._cur.execute(read_sql("get/state.sql"), (str(key.user_id),))
        result = self._cur.fetchone()
        self._conn.commit()
        return result[0] if result else None
    
    async def set_data(self, user: str, data: Dict[str, Any]) -> None:
        dataJSON = json.dumps(data, ensure_ascii=False)
        self._cur.execute(read_sql("change/data.sql"), (user,dataJSON,user,user,dataJSON))
        self._conn.commit()
        
    async def get_data(self, user: str) -> Dict[str, Any]:
        self._cur.execute(read_sql("get/data.sql"), (user,))
        result = self._cur.fetchone()
        self._conn.commit()
        if result is None:
            return {}
        return result[0]

    async def close(self):
        if self._cur:
            self._cur.close()
        if self._conn:
            self._conn.close()