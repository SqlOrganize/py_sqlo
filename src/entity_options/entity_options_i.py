

from abc import ABC, abstractmethod

class EntityOptionsI(ABC):
    
    @abstractmethod
    def pf(self):
        pass

    @abstractmethod
    def pt(self):
        pass
    
    @abstractmethod
    def call_fields(self, field_names: list[str], method:str):
        pass
    
    @abstractmethod
    def call(self, method:str):
        pass
    
    @abstractmethod
    def to_fields(self, field_names: list[str], method:str) -> dict: 
        pass
    
    @abstractmethod
    def to_(self, method:str) -> dict: 
        pass

    @abstractmethod
    def from_fields(self, row: dict, field_names: list[str], method:str) -> list: 
        pass
    
    @abstractmethod        
    def from_(self, row: dict, method:str) -> list: 
        pass


