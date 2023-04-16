from abc import ABC, abstractmethod

from py_sqlo.src.entity_options.mapping_i import MappingI
from .entity_options.entity_options_i import EntityOptionsI
from .entity_tools_i import EntityToolsI
from .entity_i import EntityI
from .field_i import FieldI

class ContainerI(ABC):
    """ Container interface.
    Para evitar redundancia ciclica
    ContainerI se utiliza en el conjunto de clases: Entity, Field, etc.
    ContainerI solamente utiliza FieldI, EntityI, etc.
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
    def tree(cls, entity_name: str) -> dict:
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
    def entity(cls, entity_name:str) -> EntityI:
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

    @classmethod
    @abstractmethod
    def explode_field(cls, entity_name:str, field_name:str) -> dict:
        pass 

    @classmethod
    @abstractmethod
    def field_by_id(cls, entity_name:str, field_id:str) -> FieldI:
        pass

    @classmethod
    @abstractmethod
    def mapping(cls, entity_name:str, field_id:str) -> MappingI:
        pass

    @classmethod
    @abstractmethod
    def tools(cls, entity_name) -> EntityToolsI:
        pass