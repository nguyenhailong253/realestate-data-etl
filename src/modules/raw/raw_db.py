from sqlalchemy import (
    MetaData, Table, insert, select, and_, update
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import Connection

from src.db.db_connection import DbConnection
from src.db.config import RAW_SCHEMA, RAW_DATA_TABLE


class RawDb:
    def __init__(self, engine: Engine, connection: Connection):
        self.engine = engine
        self.conn = connection
        self.schema = MetaData(schema=RAW_SCHEMA)
        self.table = self.connect_table()

    def connect_table(self) -> Table:
        return Table(
            RAW_DATA_TABLE, self.schema, autoload=True, autoload_with=self.engine)

    def select_all(self):
        # results = [{**row} for row in item]  # https://stackoverflow.com/a/56098483
        # return self.conn.execute(select([self.table])).fetchall()
        return self.conn.execute(select([self.table])).first()
