from agents import BaseAgent
from model.base import LLM


class GraphCreator(BaseAgent):
    def __init__(self, model: LLM):
        super().__init__(model)
