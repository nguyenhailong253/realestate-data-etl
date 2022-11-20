import os

DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_CONN_POOL_SIZE = 50

RAW_SCHEMA = "raw"
RAW_DATA_TABLE = "propertylistings"

TRANSFORMED_SCHEMA = "transformed"
STATES_AND_TERRITORIES_TABLE = "states_and_territories"
SUBURBS_TABLE = "suburbs"
REAL_ESTATE_PROPERTY_TABLE = "real_estate_property"
REAL_ESTATE_AGENTS_TABLE = "real_estate_agents"
REAL_ESTATE_AGENCIES_TABLE = "real_estate_agencies"
LISTINGS_TABLE = "listings"
ADDRESSES_TABLE = "addresses"
