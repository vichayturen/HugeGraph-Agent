from enum import Enum
from typing import List, Dict

from pyhugegraph.client import PyHugeClient

from agents import IntentRecognizer, GremlinExecutor, TripleExtractor, GraphCreator, Chatter
from model.base import LLM
from stack.agent_stack import AgentStack, AgentStepType


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"
    TOOL = "tool"


class HugeGraphAgent:
    def __init__(self, model: LLM, client: PyHugeClient):
        """

        :param model:
        :param client:
        :param print_prompt:
        :param print_model_response:
        """
        intentions = [
            "Execute gremlin",
            "Create graph",
            "Add data",
            "Just chat",
            "End conversation"
        ]
        self.model = model
        self.client = client
        self.agent_stack = AgentStack()
        self.agent_stack.push(IntentRecognizer(self.model, intentions, [], max_step=100))
        self.history = []

    def step(self, inp: str, history: List[Dict[str, str]] = None) -> str:
        response = self.agent_stack.act(inp, history)
        self.history.extend([{"role": Role.USER.value, "content": inp}, {"role": Role.ASSISTANT.value, "content": response}])
        return response
