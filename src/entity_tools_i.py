

from abc import ABC, abstractmethod

class EntityToolsI(ABC):
    
    @abstractmethod
    def field_names(self) -> list[str]:
        pass