from sqlalchemy import (
    MetaData, Table, insert, select, and_, update
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import Connection

from src.db.db_connection import DbConnection
from src.db.config import TRANSFORMED_SCHEMA, STATES_AND_TERRITORIES_TABLE


class StatesTerritoriesDb:
    def __init__(self, engine: Engine, connection: Connection):
        self.engine = engine
        self.conn = connection
        self.schema = MetaData(schema=TRANSFORMED_SCHEMA)
        self.table = self.connect_table()
        self.states = [{**row} for row in self.select_all()]

    def connect_table(self) -> Table:
        return Table(
            STATES_AND_TERRITORIES_TABLE, self.schema, autoload=True, autoload_with=self.engine)

    def select_all(self):
        """SELECT * FROM states_territories_table

        Returns:
            _type_: all rows in table
        """
        # results = [{**row} for row in item]  # https://stackoverflow.com/a/56098483
        return self.conn.execute(select([self.table])).fetchall()
