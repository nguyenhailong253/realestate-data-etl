from sqlalchemy import (
    MetaData, Table, insert, select, and_, update
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import Connection

from src.db.db_connection import DbConnection
from src.db.config import TRANSFORMED_SCHEMA, ADDRESSES_TABLE


class AddressesDb:
    def __init__(self, engine: Engine, connection: Connection):
        self.engine = engine
        self.conn = connection
        self.schema = MetaData(schema=TRANSFORMED_SCHEMA)
        self.table = self.connect_table()

    def connect_table(self) -> Table:
        return Table(
            ADDRESSES_TABLE, self.schema, autoload=True, autoload_with=self.engine)

    def select_one(self,
                   suburb_id: int,
                   unit_number: str,
                   street_number: str,
                   street_name: str,
                   street_type: str) -> int:
        query = select([self.table.columns.id]).where(
            and_(self.table.columns.suburb_id == suburb_id,
                 self.table.columns.unit_number == unit_number,
                 self.table.columns.street_number == street_number,
                 self.table.columns.street_name == street_name,
                 self.table.columns.street_type == street_type))
        return self.conn.execute(query).first()

    def insert_one(self, address: dict) -> int:
        query = insert(self.table).values(address)
        return self.conn.execute(query).inserted_primary_key
