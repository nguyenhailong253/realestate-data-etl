import dataclasses


@dataclasses.dataclass(init=True)
class Agent:
    agency_id: int
    agent_name: str  # null if agent_name == agency_name
