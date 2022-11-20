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

from src.modules.agencies.agency_transformer import AgencyTransformer

from src.modules.agents.agent_transformer import AgentTransformer

from src.modules.properties.property_transformer import PropertyTransformer


class Etl:
    def __init__(self, engine: Engine, connection: Connection):
        self.engine = engine
        self.connection = connection
        # listingsDb = ListingsDb(engine, connection)
        self.rawDb = RawDb(engine, connection)
        self.state_transformer = StateTransformer(
            StatesTerritoriesDb(engine, connection))
        self.suburb_transformer = SuburbTransformer(
            SuburbsDb(engine, connection))
        self.address_transformer = AddressTransformer(
            AddressesDb(engine, connection))
        self.agency_transformer = AgencyTransformer(
            AgenciesDb(engine, connection))
        self.agent_transformer = AgentTransformer(AgentsDb(engine, connection))
        self.property_transformer = PropertyTransformer(
            PropertiesDb(engine, connection))

    def process_suburb(self, state: str, suburb: str, postcode: str) -> int:
        # get state ID from state table
        state_id = self.state_transformer.get_state_id(state)
        # populate suburb table with state FK
        suburb = Suburb(state_and_territory_id=state_id,
                        suburb_name=suburb,
                        postcode=postcode)
        return self.suburb_transformer.get_or_create_suburb_id(suburb)

    def process_address(self, suburb_id: int, raw_data: RawListing) -> int:
        return self.address_transformer.get_or_create_address_id(
            suburb_id, raw_data.address, raw_data.gps_coordinates, raw_data.google_maps_location_url)

    def process_agency(self, raw_data: RawListing) -> int:
        return self.agency_transformer.get_or_create_agency_id(
            raw_data.agency_name, raw_data.agency_logo, raw_data.agency_property_listings_url, raw_data.agency_address)

    def process_agent(self, agency_id: int, agency_name: str, agent_name: str) -> int:
        return self.agent_transformer.get_or_create_agent_id(agency_id, agency_name, agent_name)

    def process_property(self, address_id: int, raw_data: RawListing) -> int:
        return self.property_transformer.get_or_create_property_id(
            address_id=address_id,
            id_on_tenantapp=raw_data.property_id,
            num_bedrooms=raw_data.num_bedrooms,
            num_bathrooms=raw_data.num_bathrooms,
            num_garages=raw_data.num_garages,
            property_features=raw_data.property_features)

    def run(self):
        # get data from raw
        print("Getting data from raw table...")
        raw_data = RawListing(**self.rawDb.select_all())
        suburb_id = self.process_suburb(
            raw_data.state_and_territory, raw_data.suburb, raw_data.postcode)
        print(f"Got suburb id: {suburb_id}")

        # populate address table with suburb FK
        address_id = self.process_address(suburb_id, raw_data)
        print(f"Got address id: {address_id}")

        # populate agencies table
        agency_id = self.process_agency(raw_data)
        print(f"Got agency id: {agency_id}")

        # populate agent table
        agent_id = self.process_agent(
            agency_id, raw_data.agency_name, raw_data.agent_name)
        print(f"Got agent id: {agent_id}")

        # populate property table
        property_id = self.process_property(address_id, raw_data)
        print(f"Got property id: {property_id}")

        # populate listings table


if __name__ == "__main__":
    print("Creating DB connection...")
    dbConn = DbConnection()
    engine, connection = dbConn.get_engine_and_connection()
    print("Connected")

    etl = Etl(engine, connection)

    etl.run()
