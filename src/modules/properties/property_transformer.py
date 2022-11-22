from typing import List

from src.modules.properties.properties_db import PropertiesDb
from src.modules.properties.property_dataclass import Property


class PropertyTransformer:
    def __init__(self, db: PropertiesDb):
        self.db = db

    def get_or_create_property_id(self,
                                  address_id: int,
                                  id_on_tenantapp: str,
                                  num_bedrooms: str,
                                  num_bathrooms: str,
                                  num_garages: str,
                                  property_features: List[str]) -> int:
        property_data = Property(address_id, id_on_tenantapp, num_bedrooms,
                                 num_bathrooms, num_garages, property_features)
        row = self.db.select_one(
            property_data.address_id, property_data.id_on_tenantapp)
        if row:
            print("Property data already existed")
            return {**row}['id']
        else:
            print("Property data not collected, inserting...")
            new_id = self.db.insert_one(vars(property_data))
            return {**new_id}['id']
