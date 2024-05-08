import re

from common.log import logger


class PromptTemplate:
    def __init__(self, template: str):
        self.__template = template
        keys = re.findall(r"\{[^}]+}", template)
        self.__slot_map = {}
        for key in keys:
            key = key[1:-1]
            self.__slot_map[key] = key

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__slot_map:
                self.__slot_map[key] = value
            else:
                logger.warning(f"{key} not in template slot!")

    def string(self) -> str:
        return self.__template.format(**self.__slot_map)
