from dataclasses import dataclass
from typing import List, Any, Optional

from agents import BaseAgent
from enum import Enum


class AgentStepType(Enum):
    REPLACE = "replace"
    APPEND = "append"
    REMOVE = "remove"
    STATIC = "static"


@dataclass
class AgentStepOutput:
    type: AgentStepType
    response: Optional[str]  # will not response if is None
    agent: Optional[BaseAgent]  # replace or append need this parameter


@dataclass
class AgentBlock:
    agent: BaseAgent
    step: int


class AgentStack:
    def __init__(self):
        self.stack: List[AgentBlock] = []
        self.agent = None

    def pop(self):
        return self.stack.pop()

    def push(self, block: AgentBlock):
        self.stack.append(block)

    def act(self, inp: str) -> str:
        self.stack[-1].act(inp)
