from datetime import datetime
import re
from typing import Any
from ..function.to_bool import to_bool
from ..tools.logging import Log, Logging
from ..tools.validation import Validation
from ..config import UNDEFINED
from .entity_options import EntityOptions

class Values(EntityOptions):
    """
    Values of entity

    Define metodos basicos para administrar valores:
    
    -sset: Seteo con cast y formateo
    -set: Seteo directo
    -check: Validar valor
    -default: Asignar valor por defecto
    -get: Retorno directo
    -json: Transformar a json
    -sql: Transformar a sql
    """
    def __init__(self, db, entity_name: str, prefix: str = "") -> None:
        super().__init__(db, entity_name, prefix)
       
        self._logging: Logging = Logging()
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
   
    def logging(self):
        return self._logging
   
    def call_values(self, method:str):
        """
        Ejecutar metodo en todos los valores del atributo self._values

        Los metodos posibles para ejecucion no deben llevar otro parametro mas que el field_name
        """
        return self.call_fields(list(self._values.keys()), method)


    def set(self, field_name, value):
        """
        Seteo directo.

        Debe respetar el tipo.
        """
        self._values[field_name] = value

    def get(self, field_name):
        """
        Retorno directo.
        """
        return self._values[field_name]
    
    def sset(self, field_name:str, value:Any):
        """
        slow set with casting

        @example
        val.sset("nombre", "something")
        val.sset("nombre.max", "something max")
        val.sset("nombre.count", 100)
        """
        m = "sset_"+field_name.replace(".", "_")
        if hasattr(self.__class__, m) and callable(getattr(self.__class__, m)):
            return getattr(self, m)(value)

        m = self._define_sset(field_name)
        return getattr(self, m)(field_name, value)

    def _define_sset(self, field_name):
        """
        Si la funcion sset de field_name no se encuentra definida por el usuario,        
        se define en funcion de data_type
        """
        p = field_name.split(".")
       
        if len(p) == 1:
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

        m = p.pop() #se resuelve la funcion ubicada mas a la derecha, que sera la ultima en ejecutarse y la que definira el formato final
        match m: 
            case "count" | "avg" | "sum": 
                return "_sset_int"

            case "year" | "y":
                return "_sset_year"
            
            case "date" | "ym" | "hm" | "time":
                return "_sset_datetime"

            case _:
                return self._define_sset(".".join(p)); #si no resuelve, intenta nuevamente (ejemplo field.count.max, intentara nuevamente con field.count)
   
    def _sset_datetime(self, field_name, value: Any):
        """notice datetime is a subclass of date"""
        self._values[field_name] = datetime.strptime(value, '%d/%m/%y %H:%M:%S') if value and not isinstance(value, datetime) else value
        return self._values[field_name]
    
    def _sset_year(self, field_name, value: Any):
        self._values[field_name] = str(value)

    def _sset_str(self, field_name, value: Any):
        self._values[field_name] = re.sub(' +', str(value).strip())
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

    def default(self, field_name:str):
        m = "default_"+field_name.replace(".", "_")
        if hasattr(self.__class__, m) and callable(getattr(self.__class__, m)):
            return getattr(self, m)()

        default = self._define_default(field_name)
        return self.sset(field_name, default)
    
    def _define_default(self, field_name):
        """
        Si el valor por defecto de field_name no se encuentra definida por el usuario,        
        se define en funcion de data_type
        """
        p = field_name.split(".")
       
        if len(p) == 1:
            """
            traducir field_name sin funcion
            """
            field = self._db.field(self._entity_name, field_name)
            match field.data_type():
                case "date" | "datetime" | "year" | "time":
                    return "retornar fecha actual en formato json" if "cur" in field.default().lower() else field.default()

                case _:
                    return field.default()

        p.pop() #se resuelve la funcion ubicada mas a la derecha, que sera la ultima en ejecutarse y la que definira el formato final
        return self._define_default(".".join(p)) #si no resuelve, intenta nuevamente (ejemplo field.count.max, intentara nuevamente con field.count)
   
    def json(self, field_name:str):
        """
        json

        @example
        val.sset("nombre", "something")
        val.sset("nombre.max", "something max")
        val.sset("nombre.count", 100)
        """
        m = "json_"+field_name.replace(".", "_")
        if hasattr(self.__class__, m) and callable(getattr(self.__class__, m)):
            return getattr(self, m)

        m = self._define_json(field_name)
        return getattr(self, m)(field_name)
    
    def _define_json(self, field_name):
        """
        Si la funcion json de field_name no se encuentra definida por el usuario,
        se define en funcion de data_type
        """
        p = field_name.split(".")
       
        if len(p) == 1:
            """
            traducir field_name sin funcion
            """
            field = self._db.field(self._entity_name, field_name)
            match field.data_type():
                case "year" | "time" | "date" | "timestamp":
                    return "retornar datetime como json"

                case _:
                    return self.get(field_name)

        m = p.pop() #se resuelve la funcion ubicada mas a la derecha, que sera la ultima en ejecutarse y la que definira el formato final
        match m: 
            case "count" | "avg" | "sum": 
                return self.get(field_name)

            case "year" | "y" | "date" | "ym" | "hm" | "time":
                return "retornar datetime como json"

            case _:
                return self._define_json(".".join(p)); #si no resuelve, intenta nuevamente (ejemplo field.count.max, intentara nuevamente con field.count)
   
    def sql(self, field_name:str):
        """
        sql

        @example
        val.sql("some_string") # 'something'
        val.sql("some_date") # '2000-01-01'
        val.sql("some_int")  # 123
        val.sql("some_datetime") # '2000-01-01 00:00:00'
        """
        m = "sql_"+field_name.replace(".", "_")
        if hasattr(self.__class__, m) and callable(getattr(self.__class__, m)):
            return getattr(self, m)

        m = self._define_sql(field_name)
        return getattr(self, m)(field_name)
    
    def _define_sql(self, field_name):
        """
        Si la funcion sql de field_name no se encuentra definida por el usuario,
        se define en funcion de data_type
        """
        p = field_name.split(".")
       
        if len(p) == 1:
            """
            traducir field_name sin funcion
            """
            field = self._db.field(self._entity_name, field_name)
            match field.data_type():
                case "year" | "time" | "date" | "timestamp":
                    return "retornar datetime como sql"

                case "int" | "float":
                    return "_sql_number"
                
                case "bool":
                    raise "En construccion"
                
                case "date":
                    raise "En construccion"
                
                case "year":
                    raise "En construccion"
                
                case _:
                    return "_sql_str"

        m = p.pop() #se resuelve la funcion ubicada mas a la derecha, que sera la ultima en ejecutarse y la que definira el formato final
        match m: 
            case "count" | "avg" | "sum": 
                raise "En construccion"

            case _:
                return self._define_sql(".".join(p)); #si no resuelve, intenta nuevamente (ejemplo field.count.max, intentara nuevamente con field.count)
   

    def _sql_str(self, field_name):
        if not field_name in self._values and Validation.is_undefined(self._values[field_name]):
            raise "No se puede definir sql de un valor no definido"
        
        if Validation.is_none(self._values[field_name]):
            return "null"
        
        return "'{}'".format(self._db.conn().escape_string(self._values[field_name]));  
  


    def check(self, field_name:str):
        """
        Validacion
        """
        self.logging().reset_logs(field_name)

        m = "check_"+field_name.replace(".", "_")
        if hasattr(self, m) and callable(getattr(self, m)):
            return getattr(self, m)

        checks = self._define_checks(field_name)
        v = Validation(self._values[field_name])

        for check, val in checks.items():
            if hasattr(v, check) and callable(getattr(v, check)):
                return getattr(v, check)(val)
            else:
                self.logging().add_log(field_name, Log(Log.INFO, "No existe metodo de validacion",type=check))    

        for e in v.errors():
            self.logging().add_log(field_name, type=Log(e["type"], msg=e["msg"]))

        return v.is_success()
    
    def _define_checks(self, field_name):
        """
        Si la funcion sql de field_name no se encuentra definida por el usuario,
        se define en funcion de data_type
        """
        p = field_name.split(".")
       
        if len(p) == 1:
            """
            traducir field_name sin funcion
            """
            return self._db.field_config(self._entity_name, field_name)

        m = p.pop() #se resuelve la funcion ubicada mas a la derecha, que sera la ultima en ejecutarse y la que definira el formato final
        match m: 
            case "count" | "avg" | "sum": 
                raise "En construccion"

            case _:
                return self._define_checks(".".join(p)); #si no resuelve, intenta nuevamente (ejemplo field.count.max, intentara nuevamente con field.count)
   
    

