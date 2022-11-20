import dataclasses


@dataclasses.dataclass(init=True)
class Agency:
    hq_address: str
    agency_name: str
    logo_url: str
    listings_url: str
