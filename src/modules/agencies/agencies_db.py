from sqlalchemy import (
    MetaData, Table, insert, select, and_, update
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import Connection

from src.db.db_connection import DbConnection
from src.db.config import TRANSFORMED_SCHEMA, REAL_ESTATE_AGENCIES_TABLE


class AgenciesDb:
    def __init__(self, engine: Engine, connection: Connection):
        self.engine = engine
        self.conn = connection
        self.schema = MetaData(schema=TRANSFORMED_SCHEMA)
        self.table = self.connect_table()

    def connect_table(self) -> Table:
        return Table(
            REAL_ESTATE_AGENCIES_TABLE, self.schema, autoload=True, autoload_with=self.engine)

    def select_one(self,
                   agency_name: str,
                   listings_url: str) -> int:
        query = select([self.table.columns.id]).where(
            and_(self.table.columns.agency_name == agency_name,
                 self.table.columns.listings_url == listings_url))
        return self.conn.execute(query).first()

    def insert_one(self, agency: dict) -> int:
        query = insert(self.table).values(agency)
        return self.conn.execute(query).inserted_primary_key