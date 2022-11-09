from src.db.db_connection import DbConnection

from src.modules.addresses.addresses_db import AddressesDb
from src.modules.agencies.agencies_db import AgenciesDb
from src.modules.agents.agents_db import AgentsDb
from src.modules.listings.listings_db import ListingsDb
from src.modules.properties.properties_db import PropertiesDb
from src.modules.states_territories.states_territories_db import StatesTerritoriesDb
from src.modules.suburbs.suburbs_db import SuburbsDb
from src.modules.raw.raw_db import RawDb


def main():
    dbConn = DbConnection()
    engine, connection = dbConn.get_engine_and_connection()
    addressesDb = AddressesDb(engine, connection)
    agenciesDb = AgenciesDb(engine, connection)
    agentsDb = AgentsDb(engine, connection)
    listingsDb = ListingsDb(engine, connection)
    propertiesDb = PropertiesDb(engine, connection)
    statesDb = StatesTerritoriesDb(engine, connection)
    suburbsDb = SuburbsDb(engine, connection)
    rawDb = RawDb(engine, connection)


if __name__ == "__main__":
    main()
