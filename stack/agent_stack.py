from dataclasses import dataclass
from typing import List, Any, Optional, Dict

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
    response: Optional[str] = None  # will not response if is None
    agent: Optional[BaseAgent] = None  # replace or append need this parameter


class AgentStack:
    def __init__(self):
        self.stack: List[BaseAgent] = []
        self.agent = None

    def top(self):
        return self.stack[-1]

    def pop(self):
        return self.stack.pop()

    def push(self, agent: BaseAgent):
        self.stack.append(agent)

    def replace(self, agent: BaseAgent):
        self.stack[-1] = agent

    def act(self, inp: str, history: List[Dict[str, str]] = None) -> str:
        agent_step_output = self.top().act(inp, history)
        if agent_step_output.type == AgentStepType.REPLACE:
            self.replace(agent_step_output.agent)
        elif agent_step_output.type == AgentStepType.APPEND:
            self.push(agent_step_output.agent)
        elif agent_step_output.type == AgentStepType.REMOVE:
            self.pop()
        else:  # static
            pass
        while agent_step_output.response == None:
            agent_step_output = self.top().act(inp, history)
            if agent_step_output.type == AgentStepType.REPLACE:
                self.replace(agent_step_output.agent)
            elif agent_step_output.type == AgentStepType.APPEND:
                self.push(agent_step_output.agent)
            elif agent_step_output.type == AgentStepType.REMOVE:
                self.pop()
            else:  # static
                pass
        return agent_step_output.response
