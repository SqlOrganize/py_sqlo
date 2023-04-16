

from abc import ABC, abstractmethod

from .entity_options_i import EntityOptionsI

class MappingI(EntityOptionsI):
    
    @abstractmethod
    def map(self, field_name: str):
        pass


