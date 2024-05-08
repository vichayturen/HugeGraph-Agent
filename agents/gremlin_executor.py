from pyhugegraph.client import PyHugeClient

from agents.base import BaseAgent
from model.base import LLM
from prompt.base import PromptTemplate


class GremlinExecutor(BaseAgent):
    def __init__(
            self,
            model: LLM,
            confirm_gremlin: bool = False,
            **kwargs
    ):
        super().__init__(model, **kwargs)
        self.template = PromptTemplate("""You are a HugeGraph manager. You are given a user input and you need to generate the most appropriate gremlin from the following schema:
Schema: {schema}

Input: {input}
Gremlin:""")
        self.confirm_gremlin = confirm_gremlin
        self.step = 0
        self.max_step = 100

    def act(self, inp: str, client: PyHugeClient) -> str:
        # TODO: change schema to string
        self.template.update(schema=client.schema())
        self.template.update(input=inp)
        model_response = self.call_model(self.template.string())
        gremlin = self.extract_gremlin(model_response)
        if self.confirm_gremlin:
            while True:
                yes_or_no = input(f"Gremlin: {gremlin}\nIs this the correct gremlin? (y/n)").lower()
                if yes_or_no == "y" or yes_or_no == "n":
                    break
                else:
                    print("Invalid input!")
            if yes_or_no == "n":
                return ""
        g = client.gremlin()
        try:
            g.exec(gremlin)
            return f"Parsing to be"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def extract_gremlin(model_response: str) -> str:
        return model_response.split("Gremlin:")[1].strip()
