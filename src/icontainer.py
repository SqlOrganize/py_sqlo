from abc import abstractmethod

class IContainer:
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
    def tree(cls, entityName = None) -> dict:
        pass

    @classmethod
    @abstractmethod
    def relations(cls, entityName = None) -> dict:
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
    def entity(cls, entityName = None):
        pass

    @classmethod
    @abstractmethod
    def field(cls, entityName, fieldName = None):
        pass

    @classmethod
    @abstractmethod
    def tools(cls, entityName):
        pass

    @classmethod
    @abstractmethod
    def entity_query(cls, entityName):
        pass

    @classmethod
    @abstractmethod
    def field_names(cls, entityName) -> list:
        pass 

    @classmethod
    @abstractmethod
    def fields_config(cls, entityName) -> dict:
        pass 