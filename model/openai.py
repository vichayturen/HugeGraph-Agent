from typing import List, Dict

from .base import LLM


class OpenaiLLM(LLM):
    def __init__(self):
        pass

    def call(self, inp: str, history: List[Dict[str, str]] = None) -> str:
        return ""
