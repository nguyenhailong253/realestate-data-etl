from sqlalchemy import (
    MetaData, Table, insert, select, and_, update
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import Connection

from src.db.db_connection import DbConnection
from src.db.config import TRANSFORMED_SCHEMA, SUBURBS_TABLE


class SuburbsDb:
    def __init__(self, engine: Engine, connection: Connection):
        self.engine = engine
        self.conn = connection
        self.schema = MetaData(schema=TRANSFORMED_SCHEMA)
        self.table = self.connect_table()

    def connect_table(self) -> Table:
        return Table(
            SUBURBS_TABLE, self.schema, autoload=True, autoload_with=self.engine)

    def select_one(self, suburb_name: str, postcode: str) -> int:
        query = select([self.table.columns.id]).where(
            and_(self.table.columns.suburb_name == suburb_name,
                 self.table.columns.postcode == postcode))
        return self.conn.execute(query).first()

    def insert_one(self, suburb: dict) -> int:
        query = insert(self.table).values(suburb)
        return self.conn.execute(query).inserted_primary_key
