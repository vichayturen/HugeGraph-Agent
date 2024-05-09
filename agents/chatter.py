from typing import List, Dict

from agents import BaseAgent, IntentRecognizer
from model.base import LLM
from stack.agent_stack import AgentStepOutput, AgentStepType


class Chatter(BaseAgent):
    def __init__(self, model: LLM, **kwargs):
        super().__init__(model, **kwargs)
        self.intent_recognizer = IntentRecognizer(
            model=model,
            options=["User is still chatting.", "User wants to do something other."],
            agents=[None, None],
            max_step=1
        )

    def act(self, inp: str, history: List[Dict[str, str]] = None) -> AgentStepOutput:
        intent_id = self.intent_recognizer.get_intent_id(inp)
        if intent_id == 0:
            response = self.call_model(inp, history)
            return AgentStepOutput(type=AgentStepType.STATIC, response=response)
        elif intent_id == 1:
            return AgentStepOutput(type=AgentStepType.REMOVE)
        else:
            raise ValueError(f"Invalid intent id: {intent_id}")
