from abc import ABC, abstractmethod

from src.model.ientity import IEntity

class IContainer(ABC):
    """ Container interface.
    """
    @classmethod
    @abstractmethod
    def init(cls):
        pass

    @classmethod
    @abstractmethod
    def db_connect(cls):
        pass

    @classmethod
    @abstractmethod
    def db_close(cls):
        pass

    @classmethod
    @abstractmethod
    def tree(cls, entity_name = None) -> dict:
        pass

    @classmethod
    @abstractmethod
    def relations(cls, entity_name = None) -> dict:
        pass

    @classmethod
    @abstractmethod
    def entities(cls):
        pass
    
    @classmethod
    @abstractmethod
    def entity_names(cls):
        pass
    
    @classmethod
    @abstractmethod
    def entity(cls, entity_name = None) -> IEntity:
        pass

    @classmethod
    @abstractmethod
    def field(cls, entity_name, field_name = None):
        pass

    @classmethod
    @abstractmethod
    def tools(cls, entity_name):
        pass

    @classmethod
    @abstractmethod
    def entity_query(cls, entity_name):
        pass

    @classmethod
    @abstractmethod
    def field_names(cls, entity_name) -> list:
        pass 

    @classmethod
    @abstractmethod
    def fields_config(cls, entity_name) -> dict:
        pass 