import dataclasses

from src.utils.validate_field_type import validate


@dataclasses.dataclass(init=False)
class Address:
    suburb_id: int
    display_address: str
    unit_number: str
    street_number: str
    street_name: str
    street_type: str
    street_type_abbrev: str
    latitude: str
    longitude: str
    google_maps_location_url: str
