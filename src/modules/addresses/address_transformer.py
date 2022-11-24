import difflib
import re
from typing import List

from src.modules.addresses.addresses_db import AddressesDb
from src.modules.addresses.address_dataclass import Address
from src.modules.addresses.street_type_abbrev import STREET_TYPES

from src.utils.get_key_from_value import get_key_from_value

REDUNDANT_WORDS = [
    r'level(\d+)/',
    r'level (\d+)/',
    r'level (\d+) at',
    r'(\d+) bedroom/',
    r'(.* bedroom/)',
    r'the studio -',
    r'l(\d+)',
    r'(\d+)bed/',
    'unit',
    'id:',
    'car space',
    'flat',
    'cp lot',
    'berth',
    r'\sat\s',
    'the studio',
    'shop',
    'xx',
    'bedroom',
    'room',
]

GPS_TEXT = "GPS Location:"

ROAD_DIR = {
    'n': 'north',
    'nth': 'north',
    's': 'south',
    'sth': 'south',
    'e': 'east',
    'w': 'west',
}


class AddressTransformer:
    def __init__(self, db: AddressesDb):
        self.db = db

    def remove_suburb_and_redundant_words_in_address(self, raw_address: str) -> str:
        address_without_suburb = raw_address.split(',')[0]

        for word in REDUNDANT_WORDS:
            address_without_suburb = re.sub(
                word, "", address_without_suburb.lower()).strip()
            # print(f"Removing {word}, left with {address_without_suburb}")
        return " ".join(address_without_suburb.split())

    def set_unit_and_street_numbers(self, address: Address, unit_street: str):
        unit_street_nums = unit_street.split("/")
        if len(unit_street_nums) == 0:
            raise ValueError(
                f"Cannot find unit number or street number: {unit_street} in address {address.display_address}")
        elif len(unit_street_nums) == 1:
            print(f"No unit number, only street number: {unit_street}")
            address.unit_number = None
            address.street_number = unit_street_nums[0].title()
        else:
            address.unit_number = unit_street_nums[0].title()
            address.street_number = unit_street_nums[1].title()

    def set_street_type(self, address: Address, street_type: str):
        for key, value in STREET_TYPES.items():
            if street_type.title() == key or street_type.title() == value:
                address.street_type = value
                address.street_type_abbrev = key
        try:
            closest_match = difflib.get_close_matches(
                street_type, STREET_TYPES.values(), n=1, cutoff=0.8)
            if len(closest_match) > 0:
                address.street_type = closest_match[0]
                address.street_type_abbrev = get_key_from_value(
                    STREET_TYPES, closest_match[0])
            address.street_type
            address.street_type_abbrev
        except AttributeError as e:
            print(
                f"Cannot find street type for {street_type} in address {address.display_address}: {e}")
            raise

    def set_street_name(self, address: Address, street: List[str]):
        street_name = " ".join(street).title()
        address.street_name = street_name

    def check_address_has_numeric_values(self, address: str):
        if not any(char.isdigit() for char in address):
            raise ValueError(
                f"Address has no numeric values for unit or street number: {address}")

    def normalise_street_data(self, address: Address):
        raw_address = self.remove_suburb_and_redundant_words_in_address(
            address.display_address)

        self.check_address_has_numeric_values(raw_address)

        # Usually, the first component will be unit/street numbers
        # And last component will be street type
        # Anything in between is street name
        address_components = raw_address.split(" ")
        print(
            f"Normalising address - address components: {address_components}")
        if len(address_components) == 2:
            raise ValueError(
                f"Address has no street name or street type: {address.display_address}")
        self.set_unit_and_street_numbers(address, address_components[0])

        # Remove non-alphanumeric chars
        address_components[-1] = re.sub(r'\W+', '', address_components[-1])
        if address_components[-1].lower() in ROAD_DIR.keys() or address_components[-1].lower() in ROAD_DIR.values():
            self.set_street_type(address, address_components[-2])
            self.set_street_name(address, (address_components[1:-2]))
        else:
            self.set_street_type(address, address_components[-1])
            self.set_street_name(address, (address_components[1:-1]))

    def set_latitude_longitude_data(self, gps_coordinates: str, address: Address):
        # Latitude comes first, then longitude
        # https://support.google.com/maps/answer/18539?hl=en&co=GENIE.Platform%3DDesktop#:~:text=of%20a%20place-,On%20your%20computer%2C%20open%20Google%20Maps.,decimal%20format%20at%20the%20top.
        gps = re.sub(GPS_TEXT, "", gps_coordinates).strip()
        latitude_longitude = gps.split(", ")
        address.latitude = latitude_longitude[0]
        address.longitude = latitude_longitude[1]

    def get_or_create_address_id(self,
                                 suburb_id: int,
                                 raw_address: str,
                                 gps_coordinates: str,
                                 ggl_maps_url: str) -> int:
        # Initial processing
        address = Address()
        address.display_address = raw_address
        self.normalise_street_data(address)
        address.suburb_id = suburb_id
        address.google_maps_location_url = ggl_maps_url
        self.set_latitude_longitude_data(gps_coordinates, address)

        # Check if exist
        row = self.db.select_one(address.suburb_id,
                                 address.unit_number,
                                 address.street_number,
                                 address.street_name,
                                 address.street_type)
        if row:
            print("Address data already existed")
            return {**row}['id']
        else:
            print("Address data not collected, inserting...")
            new_id = self.db.insert_one(vars(address))
            return {**new_id}['id']
