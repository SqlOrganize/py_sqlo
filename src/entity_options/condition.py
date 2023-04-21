from py_sqlo.src.function.to_bool import to_bool
from ..config import APPROX, EQUAL, NONAPPROX, NONEQUAL
from .entity_options import EntityOptions

class Condition(EntityOptions):
    """
    Definir condicion a traves de 3 elementos "field, option y value" donde 
    value es un valor válido para el field

    Sintaxis MySQL, MariaDB.
    
    Ejemplo de subclase opcional:

    -class ComisionCondition(Condition):
        def numero(self):
           return '''
    some sql condition
'''

    Las subclases deben soportar la sintaxis del motor que se encuentran 
    utilizando.
    """

    def cond(self, field_name: str, option: str, value: any):
        """ 
        Verificar la existencia de metodo exclusivo, si no exite, buscar metodo
        predefinido.

        Ejemplo: 
        -condition.cond("nombre", APPROX, "something")
        -condition.cond("fecha_alta.max.y", EQUAL, "2000"); //aplicar max, luego y
        """
        m = field_name.replace(".", "_")
        if hasattr(self.__class__, m) and callable(getattr(self.__class__, m)):
            return getattr(self, m)(option, value)

        m = self._define_condition(field_name)
        return getattr(self, m)(field_name, option, value)

    def _define_condition(self, field_name):
        p = field_name.split(".")
        if len(p) == 1:
            return self._define_condition_field(field_name)

        m = p.pop() #se resuelve la funcion ubicada mas a la derecha, que sera la ultima en ejecutarse y la que definira el formato final
        return self._define_condition_func(".".join(p), m) 

    def _define_condition_field(self, field_name):
        """
        traducir field_name sin funcion
        """
        field = self._db.field(self._entity_name, field_name)
        match field.data_type():
            case "string" | "text":
                return "_quote"

            case "boolean":
                return "_boolean"

            case _:
                return "_default"

    def _define_condition_func(self, field_name, func):
        match func: 
            case "count" | "avg" | "sum": 
                return "_default"

            case "is_set" | "exists":
                return "_exists"
            
            case "y":
                return "_quote"

            case _:
                return self._define_condition(field_name); #si no resuelve, intenta nuevamente (ejemplo field.count.max, intentara nuevamente con field.count)
    
    def _default(self, field_name, option, value): 
        field = self._db.mapping(self._entity_name, self._prefix).map(field_name)
        
        c = self._exists(field, option, value)
        if c:
            return c

        c = self._approx_cast(field, option, value)
        if c:
            return c

        v = self._value(field_name, option, value)

        return "(" + field + " " + option + " " + v._sql(field_name) + ") "  
    
    def _value(self, field_name, option, value):
        v = self._db.value(self._entity_name, self._prefix)
        v._set(field_name, value)  
        if not v._check(field_name):
            raise "Valor incorrecto al definir condicion _default: " + self._entity_name + " " + field_name + " " + option + " " + value
        return v

    def _quote(self, field_name, option, value):
        field = self._db.mapping(self._entity_name, self._prefix).map(field_name)

        c = self._exists(field, option, value)
        if c:
            return c

        c = self._approx(field, option, value)
        if c:
            return c
        
        v = self._value(field_name, option, value)

        return "(" + field + " " + option + " " + v._sql(field_name) + ") "    
  
    def _boolean(self, field_name, option, value): 
        field = self._db.mapping(self._entity_name, self._prefix).map(field_name)
    
        v = self._value(field_name, option, value)

        return "(" + field + " " + option + " " + v._sql(field_name) + ") "    
  
    def _exists(self, field_name: str, option: str, value: any) ->str:
        if(not isinstance(value, bool)):
            return ""

        if option != EQUAL and option != NONEQUAL:
            raise "La combinacion field-option-value no está permitida para definir existencia: " + field_name + " " + option + " " + value

        return "(" + field_name + " IS NOT NULL) " if (value and option == EQUAL) or (not value and option == NONEQUAL) else "(" + field_name + " IS NULL) "

    def _approx_cast(self, field_name, option, value):
        if option == APPROX: 
            return "(CAST(" + field_name + " AS CHAR) LIKE '%" + value + "%' )"

        if option == NONAPPROX:
            return "(CAST(" + field_name + " AS CHAR) NOT LIKE '%" + value + "%' )"

        return ""

    def _approx(self, field_name, option, value):
        if option == APPROX: 
            return "(lower(" + field_name + ") LIKE lower('%" + value + "%'))"

        if option == NONAPPROX:
            return "(lower(" + field_name + ") NOT LIKE lower('%" + value + "%'))"
