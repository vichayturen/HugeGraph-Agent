from typing import List, Dict

from pyhugegraph.client import PyHugeClient

from agents import IntentRecognizer
from agents.base import BaseAgent
from model.base import LLM
from prompt.base import PromptTemplate
from stack.agent_stack import AgentStepOutput, AgentStepType


class GremlinExecutor(BaseAgent):
    def __init__(
            self,
            model: LLM,
            client: PyHugeClient,
            confirm_gremlin: bool = False,
            **kwargs
    ):
        super().__init__(model, **kwargs)
        self.template_1 = PromptTemplate("""You are a HugeGraph manager. You are given a user input and you need to generate the most appropriate gremlin from the following schema:
Schema: {schema}

Input: {input}
Gremlin:""")
        self.client = client
        # TODO: change schema to string
        self.template_1.update(schema=client.schema())
        self.confirm_gremlin = confirm_gremlin
        if self.confirm_gremlin:
            self.intent_recognizer = IntentRecognizer(
                model=model,
                options=["Yes, confirm to execute.", "No, gremlin has problem."],
                agents=[None, None],
                max_step=1
            )
        self.step = 0
        self.max_step = 2
        self.gremlin = None

    def act(self, inp: str, history: List[Dict[str, str]] = None) -> AgentStepOutput:
        if self.step == 0:
            return self.act_0(inp)
        elif self.step == 1:
            return self.act_1(inp)
        else:
            return AgentStepOutput(response=None, type=AgentStepType.REMOVE, agent=None)

    def act_0(self, inp: str) -> AgentStepOutput:
        self.template_1.update(input=inp)
        model_response = self.call_model(self.template.string())
        self.gremlin = self.extract_gremlin(model_response)
        if self.confirm_gremlin:
            self.step += 1
            return AgentStepOutput(
                response=f"Gremlin: {self.gremlin}\nIs this the correct gremlin?",
                type=AgentStepType.STATIC,
                agent=None)
        else:
            try:
                g = self.client.gremlin()
                g.exec(self.gremlin)
                return AgentStepOutput(response="Execute success!", type=AgentStepType.REMOVE, agent=None)
            except Exception as e:
                return AgentStepOutput(response=f"Error occurred while execute gremlin: {e}", type=AgentStepType.REMOVE, agent=None)

    def act_1(self, inp: str) -> AgentStepOutput:
        intent_id = self.intent_recognizer.get_intent_id(inp)
        if intent_id == 0:
            try:
                g = self.client.gremlin()
                g.exec(self.gremlin)
                return AgentStepOutput(response=None, type=AgentStepType.REMOVE, agent=None)
            except Exception as e:
                return AgentStepOutput(response=f"Error occurred while execute gremlin: {e}", type=AgentStepType.REMOVE, agent=None)
        else:
            return AgentStepOutput(response="Tell me what you want to do.", type=AgentStepType.REMOVE, agent=None)

    @staticmethod
    def extract_gremlin(model_response: str) -> str:
        return model_response.split("Gremlin:")[1].strip()
