from sqlalchemy import (
    MetaData, Table, insert, select, and_, update
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import Connection

from src.db.db_connection import DbConnection
from src.db.config import TRANSFORMED_SCHEMA, LISTINGS_TABLE


class ListingsDb:
    def __init__(self, engine: Engine, connection: Connection):
        self.engine = engine
        self.conn = connection
        self.schema = MetaData(schema=TRANSFORMED_SCHEMA)
        self.table = self.connect_table()

    def connect_table(self) -> Table:
        return Table(
            LISTINGS_TABLE, self.schema, autoload=True, autoload_with=self.engine)

    def select_one(self,
                   property_id: int,
                   agent_id: int,
                   id_from_raw: int,
                   posted_date: str,
                   removed_date: str) -> int:
        query = select([self.table.columns.id]).where(
            and_(self.table.columns.property_id == property_id,
                 self.table.columns.agent_id == agent_id,
                 self.table.columns.posted_date == posted_date,
                 self.table.columns.removed_date == removed_date,
                 self.table.columns.id_from_raw == id_from_raw))
        return self.conn.execute(query).first()

    def insert_one(self, listing: dict) -> int:
        query = insert(self.table).values(listing)
        return self.conn.execute(query).inserted_primary_key
