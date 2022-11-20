import dataclasses

from typing import List


@dataclasses.dataclass(init=True)
class Property:
    address_id: int
    id_on_tenantapp: str
    num_bedrooms: str
    num_bathrooms: str
    num_garages: str
    property_features: List[str]
