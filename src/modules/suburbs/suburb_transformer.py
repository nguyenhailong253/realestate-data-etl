from src.modules.suburbs.suburbs_db import SuburbsDb
from src.modules.suburbs.suburb_dataclass import Suburb


class SuburbTransformer:
    def __init__(self, db: SuburbsDb):
        self.db = db

    def get_or_create_suburb_id(self,
                                suburb_name: str,
                                postcode: str,
                                state_id: int) -> int:
        suburb = Suburb(state_id, suburb_name, postcode)
        row = self.db.select_one(suburb.suburb_name, suburb.postcode)
        if row:
            print("Suburb data already existed")
            return {**row}['id']
        else:
            print("suburb data not collected, inserting...")
            new_id = self.db.insert_one(vars(suburb))
            return {**new_id}['id']
