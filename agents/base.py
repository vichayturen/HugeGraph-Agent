from abc import ABC, abstractmethod
from typing import Callable, List, Dict

from model.base import LLM
from stack.agent_stack import AgentStepOutput
from config import print_prompt, print_model_response


class BaseAgent(ABC):
    def __init__(self, model: LLM, **kwargs):
        """
        Base class of agents.
        :param model: Function call which input and output is a string.
        """
        self.model = model

    def call_model(self, prompt: str, history: List[Dict[str, str]] = None) -> str:
        if print_prompt:
            print(f"####### User Prompt #######\n{prompt}\n####### User Prompt #######\n")
        model_response = self.model.call(prompt, history)
        if print_model_response:
            print(f"####### Model Response #######\n{model_response}\n####### Model Response #######\n")
        return model_response

    @abstractmethod
    def act(self, inp: str, history: List[Dict[str, str]] = None) -> AgentStepOutput:
        pass


class ToolsAgent(BaseAgent, ABC):
    def __init__(self, model: Callable[[str], str], tools: List[Callable], user_confirmation: bool):
        """
        The agent that selects one tool from multiple tools and calls it.
        Tools is a list of function each does not have arguments like *args or **kwargs.
        :param model: Function call which input and output is a string.
        :param tools: Tools is a list of function.
        """
        super().__init__(model)
        self.tools = [{tool.__name__: tool} for tool in tools]
        self.tool_json = [{"name": tool.__name__, "arguments": tool.__code__.co_varnames} for tool in tools]
        self.user_confirmation = user_confirmation

    @abstractmethod
    def act(self, inp: str, history: List[Dict[str, str]] = None) -> None:
        pass
