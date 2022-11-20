from src.modules.agencies.agencies_db import AgenciesDb
from src.modules.agencies.agency_dataclass import Agency


class AgencyTransformer:
    def __init__(self, db: AgenciesDb):
        self.db = db

    def get_or_create_agency_id(self,
                                agency_name: str,
                                logo_url: str,
                                listings_url: str,
                                hq_address: str) -> int:
        agency = Agency(hq_address=hq_address, agency_name=agency_name,
                        logo_url=logo_url, listings_url=listings_url)
        row = self.db.select_one(agency_name, listings_url)
        if row:
            print("Agency data already existed")
            return {**row}['id']
        else:
            print("Agency data not collected, inserting...")
            new_id = self.db.insert_one(vars(agency))
            return {**new_id}['id']
