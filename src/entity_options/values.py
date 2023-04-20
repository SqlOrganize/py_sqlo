from datetime import datetime
from typing import Any
from py_sqlo.src.function.to_bool import to_bool
from py_sqlo.src.tools.logging import Logging
from ..config import UNDEFINED
from .entity_options import EntityOptions

class Values(EntityOptions):
    """
    Values of entity
    """
    def __init__(self, db, entity_name: str, prefix: str = "") -> None:
        super().__init__(db, entity_name, prefix)
       
        self._logs: Logging = Logging()
        """
        Logs de procesamiento de valores
        """

        self._values: dict = dict()
        """
        Valores de la entidad

        Se almacenan en el formato python correspondiente, ejemplo:

        -un string se almacena como str
        -un entero como int
        -una fecha como datetime
        -etc
        """
   
    def logs(self):
        return self._logs
   
    def sset(self, field_name, value):
        """
        slow set with casting

        @example
        val.sset("nombre", "something")
        val.sset("nombre.max", "something max")
        val.sset("nombre.count", 100)
        """
        m = "sset"+field_name.replace(".", "_")
        if hasattr(self.__class__, m) and callable(getattr(self.__class__, m)):
            return getattr(self, m)(value)

        m = self._define_sset(field_name)
        return getattr(self, m)(field_name, value)

   
    def _define_sset(self, field_name):
        p = field_name.split(".")
        if len(p) == 1:
            return self._define_sset_field(field_name)

        m = p.pop() #se resuelve la funcion ubicada mas a la derecha, que sera la ultima en ejecutarse y la que definira el formato final
        return self._define_sset_func(".".join(p), m)
   
    def _define_sset_field(self, field_name):
        """
        traducir field_name sin funcion
        """
        field = self._db.field(self._entity_name, field_name)
        match field.data_type():
            case "year":
                return "_sset_year"

            case "time" | "date" | "timestamp":
                return "_sset_datetime"

            case "integer":
                return "_sset_int"
               
            case "float":
                return "_sset_float"
           
            case "boolean":
                return "_sset_bool"

            case _:
                return "_sset_str"
               
    
    def _define_sset_func(self, field_name, func):
        match func: 
            case "count" | "avg" | "sum": 
                return "_sset_int"

            case "year" | "y":
                return "_sset_year"
            
            case "date" | "ym" | "hm" | "time":
                return "_sset_datetime"

            case _:
                return self._define_sset(field_name); #si no resuelve, intenta nuevamente (ejemplo field.count.max, intentara nuevamente con field.count)

    def _sset_datetime(self, field_name, value: Any):
        """notice datetime is a subclass of date"""
        self._values[field_name] = datetime.strptime(value, '%d/%m/%y %H:%M:%S') if value and not isinstance(value, datetime) else value
        return self._values[field_name]
    
    def _sset_year(self, field_name, value: Any):
        self._values[field_name] = str(value)

    def _sset_str(self, field_name, value: Any):
        self._values[field_name] = str(value)
        return self._values[field_name]

    def _sset_int(self, field_name, value: Any):
        self._values[field_name] = int(value)
        return self._values[field_name]

    def _sset_float(self, field_name, value: Any):
        self._values[field_name] = float(value)
        return self._values[field_name]
    
    def _sset_bool(self, field_name, value: Any):
        self._values[field_name] = to_bool(value)
        return self._values[field_name]
    
    def set(self, field_name, value):
        """
        Seteo directo.

        Debe respetar el tipo.
        """
        self._values[field_name] = value
