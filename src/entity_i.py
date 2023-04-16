from abc import ABC, abstractmethod


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
    def nf(self) -> list:
        """Return a list of FieldI"""
        pass

    @abstractmethod
    def mo(self) -> list:
        """Return a list of FieldI"""
        pass

    @abstractmethod
    def oo(self) -> list:
        """Return a list of FieldI"""
        pass

    @abstractmethod
    def main(self) -> list[str]:
        pass