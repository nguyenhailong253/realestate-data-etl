import time
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

from src.modules.listings.listing_transformer import ListingTransformer


class Etl:
    def __init__(self, engine: Engine, connection: Connection):
        self.engine = engine
        self.connection = connection
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
        self.listing_transformer = ListingTransformer(
            ListingsDb(engine, connection))

    def process_suburb(self, state: str, suburb: str, postcode: str) -> int:
        # get state ID from state table
        state_id = self.state_transformer.get_state_id(state)
        # populate suburb table with state FK
        return self.suburb_transformer.get_or_create_suburb_id(
            suburb_name=suburb, postcode=postcode, state_id=state_id)

    def process_address(self, suburb_id: int, raw_data: RawListing) -> int:
        return self.address_transformer.get_or_create_address_id(
            suburb_id=suburb_id,
            raw_address=raw_data.address,
            gps_coordinates=raw_data.gps_coordinates,
            ggl_maps_url=raw_data.google_maps_location_url)

    def process_agency(self, raw_data: RawListing) -> int:
        return self.agency_transformer.get_or_create_agency_id(
            agency_name=raw_data.agency_name,
            logo_url=raw_data.agency_logo,
            listings_url=raw_data.agency_property_listings_url,
            hq_address=raw_data.agency_address)

    def process_agent(self,
                      agency_id: int,
                      agency_name: str,
                      agent_name: str) -> int:
        return self.agent_transformer.get_or_create_agent_id(
            agency_id=agency_id,
            agency_name=agency_name,
            agent_name=agent_name)

    def process_property(self, address_id: int, raw_data: RawListing) -> int:
        return self.property_transformer.get_or_create_property_id(
            address_id=address_id,
            id_on_tenantapp=raw_data.property_id,
            num_bedrooms=raw_data.num_bedrooms,
            num_bathrooms=raw_data.num_bathrooms,
            num_garages=raw_data.num_garages,
            property_features=raw_data.property_features)

    def process_listing(self, property_id: int, agent_id: int, raw_data: RawListing) -> int:
        return self.listing_transformer.get_or_create_listing_id(
            property_id=property_id,
            agent_id=agent_id,
            id_from_raw=raw_data.id,
            price=raw_data.price,
            move_in_date=raw_data.move_in_date,
            property_url=raw_data.property_url,
            ad_posted_date=raw_data.ad_posted_date,
            ad_removed_date=raw_data.ad_removed_date,
            listing_title=raw_data.listing_title,
            listing_description=raw_data.listing_description,
            property_images=raw_data.property_images)

    def mark_raw_data_as_processed(self, raw_listing_id: int):
        self.rawDb.update_etl_done_flag(raw_listing_id)
        print(f"Updated etl_done flag for row id: {raw_listing_id}")

    def run(self):
        print("Getting data from raw table...")
        rows = self.rawDb.select_all()
        print(f"Found {len(rows)} rows without ETL done\n")
        count = 0

        # 59 d minutes from now - due to 1hr time limit on CircleCI Free Plan
        timeout = time.time() + 60*59
        for row in rows:
            if time.time() > timeout:
                print(f"Reaching time limit, stopping now...")
                break
            count += 1
            start_time = time.time()
            raw_data = RawListing(**row)
            print("\n\n=================================================")
            print(
                f"{count}. Starting ETL process for property id: {raw_data.property_id}, at row id: {raw_data.id}")
            try:
                suburb_id = self.process_suburb(
                    raw_data.state_and_territory, raw_data.suburb, raw_data.postcode)
                print(f"- Suburb id: {suburb_id}")

                # populate address table with suburb FK
                address_id = self.process_address(suburb_id, raw_data)
                print(f"- Address id: {address_id}")

                # populate agencies table
                agency_id = self.process_agency(raw_data)
                print(f"- Agency id: {agency_id}")

                # populate agent table
                agent_id = self.process_agent(
                    agency_id, raw_data.agency_name, raw_data.agent_name)
                print(f"- Agent id: {agent_id}")

                # populate property table
                property_id = self.process_property(address_id, raw_data)
                print(f"- Property id: {property_id}")

                # populate listings table
                listing_id = self.process_listing(
                    property_id, agent_id, raw_data)
                print(f"- Listing id: {listing_id}")

                self.mark_raw_data_as_processed(raw_data.id)
                print(
                    f"Done ETL for id: {raw_data.property_id}, at row id: {raw_data.id}, took {time.time() - start_time}s")
                print("=================================================")
            except Exception as e:
                print(
                    f"Failed to process data for property id: {raw_data.property_id}, at row id: {raw_data.id} with address: {raw_data.address}\n{e}")


if __name__ == "__main__":
    print("Creating DB connection...")
    dbConn = DbConnection()
    engine, connection = dbConn.get_engine_and_connection()
    print("Connected")

    etl = Etl(engine, connection)

    etl.run()
