from sqlalchemy import (
    MetaData, Table, insert, select, and_, update
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import Connection

from src.db.db_connection import DbConnection
from src.db.config import TRANSFORMED_SCHEMA, REAL_ESTATE_PROPERTIES_TABLE


class PropertiesDb:
    def __init__(self, engine: Engine, connection: Connection):
        self.engine = engine
        self.conn = connection
        self.schema = MetaData(schema=TRANSFORMED_SCHEMA)
        self.table = self.connect_table()

    def connect_table(self) -> Table:
        return Table(
            REAL_ESTATE_PROPERTIES_TABLE, self.schema, autoload=True, autoload_with=self.engine)

    def select_one(self, address_id: int) -> int:
        query = select([self.table.columns.id]).where(
            self.table.columns.address_id == address_id)
        return self.conn.execute(query).first()

    def insert_one(self, property_data: dict) -> int:
        query = insert(self.table).values(property_data)
        return self.conn.execute(query).inserted_primary_key
