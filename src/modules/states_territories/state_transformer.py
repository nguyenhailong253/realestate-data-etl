from src.modules.states_territories.states_territories_db import StatesTerritoriesDb


class StateTransformer:
    def __init__(self, db: StatesTerritoriesDb):
        self.db = db

    def get_state_id(self, raw_state: str) -> int:
        for state in self.db.states:
            if raw_state.upper() == state['state_code'] or raw_state.upper() == state['state_name']:
                return state['id']
        raise ValueError(f"Cannot find state id for raw state: {raw_state}")
