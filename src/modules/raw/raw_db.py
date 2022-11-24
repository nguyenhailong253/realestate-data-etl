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
        query = select([self.table]).where(
            and_(self.table.columns.off_market == True,
                 self.table.columns.etl_done == False,
                 self.table.columns.ad_removed_date != None))  # .limit(10)
        return self.conn.execute(query).fetchall()

    def update_etl_done_flag(self, raw_listing_id: int):
        query = update(self.table).values(etl_done=True).where(
            self.table.columns.id == raw_listing_id)
        self.conn.execute(query)
