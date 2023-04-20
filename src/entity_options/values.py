from py_sqlo.src.tools.logging import Logging
from ..config import UNDEFINED
from .entity_options import EntityOptions

class Values(EntityOptions):
    """
    Values of entity
    """
    def __init__(self, db, entity_name: str, prefix: str = "") -> None:
        super().__init__(entity_name, prefix)
       
        self.db = db

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
        m = field_name.replace(".", "_")
        if hasattr(self.__class__, m) and callable(getattr(self.__class__, m)):
            return getattr(self, m)(value)

        m = self._define_set(field_name)
        return getattr(self, m)(field_name, option, value)

   
    def _define_set(self, field_name):
        p = field_name.split(".")
        if len(p) == 1:
            return self._define_set_field(field_name)

        m = p.pop() #se resuelve la funcion ubicada mas a la derecha, que sera la ultima en ejecutarse y la que definira el formato final
        return self._define_set_func(".".join(p), m)
   
    def _define_set_field(self, field_name):
        """
        traducir field_name sin funcion
        """
        field = self.db.field(self._entity_name, field_name)
        match field.data_type():
            case "year":
                return "_set_year"

            case "time" | "date" | "timestamp":
                return "_set_datetime"

            case "int":
                return "_set_int"
               
            case "float":
                return "_set_float"
           
            case "boolean":
                return "_set_bool"

            case _:
                return "_set_str"
               
    
    def _define_set_func(self, field_name, func):
        match func: 
            case "count" | "avg" | "sum": 
                return "_set_int"

            case "year" | "y":
                return "_set_year"
            
            case "date" | "ym" | "hm" | "time":
                return "_set_datetime"

            case _:
                return self._define_set(field_name); #si no resuelve, intenta nuevamente (ejemplo field.count.max, intentara nuevamente con field.count)


   
   
   