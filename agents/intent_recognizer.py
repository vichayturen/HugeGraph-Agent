import re
from typing import List

from agents.base import BaseAgent
from model.base import LLM
from prompt.base import PromptTemplate
from stack.agent_stack import AgentStepOutput, AgentStepType


class IntentRecognizer(BaseAgent):
    def __init__(self, model: LLM, options: List[str], agents: List[BaseAgent], **kwargs):
        super().__init__(model, **kwargs)
        self.options = options
        self.agents = agents
        self.template = PromptTemplate("""You are an intent recognizer. You are given a user input and you need to choose the most appropriate intent from the following options:
{options}

Input: {input}
Intent:""")
        option_string = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(options)])
        self.template.update(options=option_string)
        self.step = 0
        self.max_step = 100

    def act(self, inp: str) -> AgentStepOutput:
        self.step += 1
        if self.step > self.max_step:
            return AgentStepOutput(response="Sorry, conversation should be shutdown!",
                                   type=AgentStepType.REMOVE, agent=None)
        self.template.update(input=inp)
        model_response = self.call_model(self.template.string())
        intent_id = self.extract_intent(model_response)
        if 1 <= intent_id <= len(self.options):
            return AgentStepOutput(response=None, type=AgentStepType.APPEND, agent=self.agents[intent_id - 1])
        return AgentStepOutput(response="Sorry, may you tell me more details about what you want me to do?",
                               type=AgentStepType.STATIC, agent=None)

    @staticmethod
    def extract_intent(model_response: str) -> int:
        return int(re.search(r"\d+", model_response).groups())
