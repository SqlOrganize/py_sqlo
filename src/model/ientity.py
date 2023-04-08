from abc import ABC, abstractmethod

class IEntity(ABC):
    """ 
    Entity interface.
    Se define para evitar "circular dependencies" 
    """
    @abstractmethod
    def n_(self):
        pass

    @abstractmethod
    def unique(self) -> list:
        pass

    @abstractmethod
    def unique_multiple(self) -> list:
        pass