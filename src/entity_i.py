from abc import ABC, abstractmethod

from .field_i import FieldI

class EntityI(ABC):
    """ 
    Entity interface.
    Utilizada solamente en IContainer y como superclase de Entity
    """
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def unique(self) -> list:
        pass

    @abstractmethod
    def unique_multiple(self) -> list:
        pass

    @abstractmethod
    def alias(self) -> str:
        pass

    @abstractmethod
    def identifier(self) -> list[str]:
        pass

    @abstractmethod
    def nf(self) -> list[FieldI]:
        pass

    @abstractmethod
    def main(self) -> list[str]:
        pass