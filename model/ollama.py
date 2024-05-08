from typing import List, Dict

import requests

from .base import LLM


class OllamaLLM(LLM):
    def __init__(self, model: str, host: str = "localhost", port: int = 11434):
        self.model = model
        self.host = host
        self.port = port

    def call(self, inp: str, history: List[Dict[str, str]] = None) -> str:
        if history is None:
            history = []
        history.append({"role": "user", "content": inp})
        data = {"model": self.model, "messages": history, "stream": False}
        response = requests.post(
            f"http://{self.host}:{self.port}/api/chat",
            headers={"Content-Type": "application/json"},
            json=data
        )
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            raise Exception(f"Error: {response.status_code}")
