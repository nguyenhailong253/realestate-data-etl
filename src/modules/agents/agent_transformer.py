from typing import List

from src.modules.agents.agents_db import AgentsDb
from src.modules.agents.agent_dataclass import Agent


class AgentTransformer:
    def __init__(self, db: AgentsDb):
        self.db = db

    def get_or_create_agent_id(self,
                               agency_id: int,
                               agency_name: str,
                               agent_name: str) -> int:
        # Sometimes they use agency name instead of an agent's name
        # in this case we keep agent_name as None and just reference agency db record directly
        name = None if agency_name == agent_name else agent_name
        agent = Agent(agency_id, name)
        row = self.db.select_one(agency_id, name)
        if row:
            print("Agent data already existed")
            return {**row}['id']
        else:
            print("Agent data not collected, inserting...")
            new_id = self.db.insert_one(vars(agent))
            return {**new_id}['id']
