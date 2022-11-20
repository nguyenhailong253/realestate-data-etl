from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import Connection

from src.db.db_connection import DbConnection

from src.modules.addresses.addresses_db import AddressesDb
from src.modules.agencies.agencies_db import AgenciesDb
from src.modules.agents.agents_db import AgentsDb
from src.modules.listings.listings_db import ListingsDb
from src.modules.properties.properties_db import PropertiesDb
from src.modules.states_territories.states_territories_db import StatesTerritoriesDb
from src.modules.suburbs.suburbs_db import SuburbsDb
from src.modules.raw.raw_db import RawDb

from src.modules.raw.raw_listing_dataclass import RawListing


from src.modules.states_territories.state_transformer import StateTransformer
from src.modules.suburbs.suburb_transformer import SuburbTransformer
from src.modules.suburbs.suburb_dataclass import Suburb

from src.modules.addresses.address_transformer import AddressTransformer
from src.modules.addresses.address_dataclass import Address


class Etl:
    def __init__(self, engine: Engine, connection: Connection):
        self.engine = engine
        self.connection = connection
        # agenciesDb = AgenciesDb(engine, connection)
        # agentsDb = AgentsDb(engine, connection)
        # listingsDb = ListingsDb(engine, connection)
        # propertiesDb = PropertiesDb(engine, connection)
        self.rawDb = RawDb(engine, connection)
        self.state_transformer = StateTransformer(
            StatesTerritoriesDb(engine, connection))
        self.suburb_transformer = SuburbTransformer(
            SuburbsDb(engine, connection))
        self.address_transformer = AddressTransformer(
            AddressesDb(engine, connection))

    def process_suburb(self, state: str, suburb: str, postcode: str) -> int:
        # get state ID from state table
        state_id = self.state_transformer.get_state_id(state)
        # populate suburb table with state FK
        suburb = Suburb(state_and_territory_id=state_id,
                        suburb_name=suburb,
                        postcode=postcode)
        return self.suburb_transformer.get_or_create_suburb_id(suburb)

    def run(self):
        # get data from raw
        print("Getting data from raw table...")
        raw_data = RawListing(**self.rawDb.select_all())
        suburb_id = self.process_suburb(
            raw_data.state_and_territory, raw_data.suburb, raw_data.postcode)
        print(f"Got suburb id: {suburb_id}")

        # populate address table with suburb FK
        address_id = self.address_transformer.get_or_create_address_id(
            suburb_id, raw_data.address, raw_data.gps_coordinates, raw_data.google_maps_location_url)

        print(f"Got address id: {address_id}")
        # populate agencies table
        # populate property table and agent table first
        # populate listings table


if __name__ == "__main__":
    print("Creating DB connection...")
    dbConn = DbConnection()
    engine, connection = dbConn.get_engine_and_connection()
    print("Connected")

    etl = Etl(engine, connection)

    etl.run()
