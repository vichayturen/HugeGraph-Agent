from typing import List, Dict

from pyhugegraph.client import PyHugeClient

from agents.base import BaseAgent
from model.base import LLM
from prompt.base import PromptTemplate
from stack.agent_stack import AgentStepOutput, AgentStepType


class TripleExtractor(BaseAgent):
    def __init__(self, model: LLM, client: PyHugeClient, confirm_triples: bool = False, **kwargs):
        super().__init__(model, **kwargs)
        self.template = PromptTemplate("""You are an intent recognizer. You are given a user input and you need to choose the most appropriate intent from the following options:
{schema}

Input: {input}
Intent:""")
        self.client = client
        # TODO: load schema from hugegraph
        self.template.update(schema=client.schema())
        self.confirm_triples = confirm_triples

    def act(self, inp: str, history: List[Dict[str, str]] = None) -> AgentStepOutput:
        self.template.update(input=inp)
        model_response = self.call_model(self.template.string())
        return AgentStepOutput(type=AgentStepType.REMOVE, response=model_response, agent=None)

    @staticmethod
    def extract_triple(model_response: str) -> list[tuple]:
        return []
