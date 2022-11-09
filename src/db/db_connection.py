from sqlalchemy import (
    create_engine, MetaData, Table, insert, select, and_, update
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import Connection

from src.db.config import (
    DB_USERNAME,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_CONN_POOL_SIZE,
)


class DbConnection:
    """Create 1 instance of this class and just pass it around
    """

    def __init__(self):
        self.dbEngine: Engine = self.create_db_engine()
        self.conn: Connection = self.dbEngine.connect()

    def create_db_engine(self) -> Engine:
        dbUrl = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        return create_engine(dbUrl, pool_size=DB_CONN_POOL_SIZE)

    def get_engine_and_connection(self) -> tuple[Engine, Connection]:
        return (self.dbEngine, self.conn)
