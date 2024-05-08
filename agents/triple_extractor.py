from agents.base import BaseAgent
from model.base import LLM
from prompt.base import PromptTemplate


class TripleExtractor(BaseAgent):
    def __init__(self, model: LLM, confirm_triple: bool = False, **kwargs):
        super().__init__(model, **kwargs)
        self.template = PromptTemplate("""You are an intent recognizer. You are given a user input and you need to choose the most appropriate intent from the following options:
{schema}

Input: {input}
Intent:""")
        self.confirm_triple = confirm_triple

    def act(self, inp: str) -> str:
        self.template.update(input=inp)
        model_response = self.call_model(self.template.string())
        return ""

    @staticmethod
    def extract_triple(model_response: str) -> list[tuple]:
        return []
