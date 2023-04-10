
from abc import ABC, abstractmethod

class IField(ABC):
    """
    Utilizada solamente en IContainer y como superclase de Field
    """
    @abstractmethod
    def name(self):
        pass

    @abstractmethod       
    def alias(self):  
        pass

    @abstractmethod
    def entity_name(self):
        pass

    @abstractmethod
    def entity_ref_name(self):
        pass

    @abstractmethod
    def entity(self):
        pass

    @abstractmethod
    def entity_ref(self):
        pass
    
    @abstractmethod
    def is_main(self):
        pass


