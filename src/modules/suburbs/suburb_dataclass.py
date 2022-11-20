import dataclasses

from src.utils.validate_field_type import validate


@dataclasses.dataclass(init=True)
class Suburb:
    state_and_territory_id: int
    suburb_name: str
    postcode: str

    def __post_init__(self):
        validate(self)
        self.suburb_name = self.suburb_name.title()
