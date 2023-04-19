from py_sqlo.src.tools.logging import Logging
from ..config import UNDEFINED
from .entity_options import EntityOptions

class Values(EntityOptions):
    """ 
    Values of entity
    """
    def __init__(self, entity_name: str, prefix: str = "") -> None:
        super().__init__(entity_name, prefix)
        
        self._logs: Logging = Logging()
        """
        Logs de procesamiento de valores
        """

        self._values = []
        """
        Valores de la entidad
        """
    
    def logs(self):
        return self._logs
    

    def set(self, field_name, value):
        """
        @example
        val.set("nombre", "something")
        val.set("nombre.max", "something max")
        val.set("nombre.count", 100)
        """

       
   