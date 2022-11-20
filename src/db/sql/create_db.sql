-- Create table for states
create table if not exists transformed.states_and_territories (
	id bigserial PRIMARY KEY,
	state_code varchar(5), -- ENUM
	state_name varchar(50), -- ENUM
	country varchar(60) -- https://www.worldatlas.com/articles/what-is-the-longest-country-name-in-the-world.html
)

-- Create table for suburbs
create table if not exists transformed.suburbs (
	id bigserial PRIMARY KEY,
	state_and_territory_id bigint, -- FK
	suburb_name varchar(50), -- ENUM
	postcode varchar(10)
)


ALTER TABLE transformed.states_and_territories ALTER COLUMN state_name TYPE varchar (50);
ALTER TABLE transformed.real_estate_agencies ADD COLUMN hq_address TEXT;
ALTER TABLE transformed.real_estate_agents DROP COLUMN listings_url;
ALTER TABLE IF EXISTS transformed.real_estate_property RENAME TO real_estate_properties;

-- for addresses, ignore addressLine1 or 2 pattern for now, i.e ignore building name and stuff for now
-- usually line1 is for building name, line 2 is the physical address

-- Create table for addresses
create table if not exists transformed.addresses (
	id bigserial PRIMARY KEY,
	suburb_id bigint, -- FK
	display_address varchar(255),
	unit_number varchar(10), -- e.g 15
	street_number varchar(20), -- e.g 1
	street_name varchar(100), -- e.g Swanston
	street_type varchar(50), -- Street, Road, Court, etc
	-- https://meteor.aihw.gov.au/content/270020 
	-- https://meteor.aihw.gov.au/content/429840
	-- https://meteor.aihw.gov.au/content/429387
	-- https://www.stylemanual.gov.au/grammar-punctuation-and-conventions/names-and-terms/australian-place-names
	-- add a street_type for unknown - there's a type called Way, abbrev as WY
	street_type_abbrev varchar(10), -- e.g St, Rd, etc  -- ENUM
	latitude varchar(20),
	longitude varchar(20),
	google_maps_location_url text
)

-- Create table for property
create table if not exists transformed.real_estate_properties (
	id bigserial PRIMARY KEY,
	address_id bigint, -- FK
	id_on_tenantapp varchar(50),
	num_bedrooms varchar(2),
	num_bathrooms varchar(2),
	num_garages varchar(2),
	property_features varchar(50)[]
)

-- Create table for property listings
create table if not exists transformed.listings (
	id bigserial PRIMARY KEY,
	property_id bigint, -- FK
	agent_id bigint, -- FK
	id_from_raw bigint,
	price_per_week varchar(5), -- do not include $ sign
	price_per_month varchar(6), -- do not include $ sign
	move_in_date varchar(20),
	listing_url varchar(100),
	posted_date timestamp,
	removed_date timestamp,
	listing_title text,
	listing_description text,
	images text[], -- list of urls
	on_market boolean, -- true or false
	listing_purpose varchar(20) -- rental or sale/commercial
)

-- Create table for real estate agents
create table if not exists transformed.real_estate_agents (
	id bigserial PRIMARY KEY,
	agency_id bigint, -- FK
	agent_name varchar(100), -- null if agent_name == agency_name
)

-- Create table for real estate agencies
create table if not exists transformed.real_estate_agencies (
	id bigserial PRIMARY KEY,
	agency_name varchar(200),
	logo_url text,
	listings_url text,
	hq_address text,
)

-- need to create index for each foreign key
create index idx_property_id on raw.propertylistings(property_id)
