from typing import List, Dict

from agents import BaseAgent
from model.base import LLM


class Chatter(BaseAgent):
    def __init__(self, model: LLM, **kwargs):
        super().__init__(model, **kwargs)

    def act(self, inp: str, history: List[Dict[str, str]] = None) -> str:
        return self.call_model(inp, history)
