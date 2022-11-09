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
