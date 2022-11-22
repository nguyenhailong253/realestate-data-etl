import dataclasses
from typing import List


@dataclasses.dataclass(init=False)
class Listing:
    property_id: int
    agent_id: int
    id_from_raw: int
    price_per_week: str
    price_per_month: str
    move_in_date: str
    listing_url: str
    posted_date: str
    removed_date: str
    listing_title: str
    listing_description: str
    images: List[str]
    listing_purpose: str
