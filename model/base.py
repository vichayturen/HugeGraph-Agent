from abc import ABC, abstractmethod
from typing import Dict, List


class LLM(ABC):
    @abstractmethod
    def call(self, inp: str, history: List[Dict[str, str]] = None) -> str:
        pass
