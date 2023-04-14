import importlib
import socket

from py_sqlo.src.function.snake_case_to_camel_case import snake_case_to_camel_case
from py_sqlo.src.entity_options.mapping_test import MappingTest


class ContainerTest():
    """ Dependency injection cls.
    """
    _mapping:dict = dict()
    "instances of Mapping"

    @classmethod
    def mapping(cls, entity_name: str, prefix: str = ""):
        if entity_name in cls._mapping:
            return cls._mapping[entity_name]

        try:
            m = importlib.import_module("src.mapping."+entity_name)
            Mapping_ = getattr(m, snake_case_to_camel_case(entity_name)+"Mapping")
            cls._mapping[entity_name] = Mapping_(prefix)

        except ModuleNotFoundError:
            cls._mapping[entity_name] = MappingTest(entity_name, prefix)
        
        return cls._mapping[entity_name]
