
from abc import ABC, abstractmethod

from py_sqlo.src.entity_i import EntityI

class FieldI(ABC):
    """
    Utilizada solamente en IContainer y como superclase de Field
    """
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod       
    def alias(self) -> str:  
        pass

    @abstractmethod
    def entity(self) -> EntityI:
        pass

    @abstractmethod
    def is_main(self) -> bool:
        pass

    @abstractmethod
    def entity_ref(self) -> EntityI:
        pass
    


