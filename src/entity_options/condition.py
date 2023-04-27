from ..function.to_bool import to_bool
from .entity_options import EntityOptions
from .._mysql.options import OPTIONS

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

    def cond(self, field_name: str, option: str, value: any) -> dict:
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

    def _value(self, field_name, value):
        v = self._db.values(self._entity_name, self._prefix)

        v.sset(field_name, value)

        if not v.check(field_name):
            raise "Valor incorrecto al definir condicion: " + self._entity_name + " " + field_name + "  " + value
        
        return v.sql(field_name)

    def _define_condition(self, field_name):
        p = field_name.split(".")
        if len(p) == 1:
            field = self._db.field(self._entity_name, field_name)
            match field.type():
                case "str":
                    return "_str"

                case "bool":
                    return "_bool"

                case _:
                    return "_default"

        m = p.pop() #se resuelve la funcion ubicada mas a la derecha, que sera la ultima en ejecutarse y la que definira el formato final
        match m: 
            case "count" | "avg" | "sum": 
                return "_default"

            case "is_set" | "exists":
                return "_exists"
            
            case "y":
                return "_str"

            case _:
                return self._define_condition(field_name); #si no resuelve, intenta nuevamente (ejemplo field.count.max, intentara nuevamente con field.count)

    
    def _default(self, field_name, opt, value): 
        field = self._db.mapping(self._entity_name, self._prefix).map(field_name)
        
        c = self._exists(field, opt, value)
        if c["sql"]:
            return c

        c = self._approx_cast(field, opt, value)
        if c["sql"]:
            return c

        return {
            "sql":"(" + field + " " + OPTIONS[opt] + " %s) ",
            "params":(self._value(field_name, value), )
        }
    
    def _str(self, field_name, opt, value) -> tuple:
        field = self._db.mapping(self._entity_name, self._prefix).map(field_name)

        c = self._exists(field, opt, value)
        if c["sql"]:
            return c

        c = self._approx(field, opt, value)
        if c["sql"]:
            return c
        
        return {
            "sql":"(" + field + " " + OPTIONS[opt] + " %s) ",
            "params":(self._value(field_name, value), )
        }
    
    def _bool(self, field_name, option, value): 
        field = self._db.mapping(self._entity_name, self._prefix).map(field_name)

        return {
            "sql":"(" + field + " " + OPTIONS[option] + " %s) ",
            "params":(self._value(field_name, value), )
        }

    def _exists(self, field_name: str, option: str, value: any) -> tuple:
        if(not isinstance(value, bool)):
            return { "sql":"", "params":() }
        
        if option != "EQUAL" and option != "NONEQUAL":
            raise "La combinacion field-option-value no está permitida para definir existencia: " + field_name + " " + option + " " + value

        return {
            "sql":"(" + field_name + " IS NOT NULL) ",
            "params":()
        } if (value and option == "EQUAL") or (not value and option == "NONEQUAL") else {
            "sql":"(" + field_name + " IS NULL) ",
            "params":()
        }

    def _approx_cast(self, field_name, option, value):
        if option == "APPROX": 
            return {
                "sql":"(LOWER(CAST(" + field_name + " AS CHAR)) LIKE LOWER(%s)) ",
                "params":("%" + value + "%", )
            }

        if option == "NONAPPROX":
            return {
                "sql":"(LOWER(CAST(" + field_name + " AS CHAR)) NOT LIKE LOWER(%s)) ",
                "params":("%" + value + "%", )
            }

        return { "sql":"", "params":() }

    def _approx(self, field_name, option, value) -> tuple:
        if option == "APPROX": 
            return {
                "sql":"(lower(" + field_name + ") LIKE lower(%s)) ",
                "params":("%" + value + "%", )
            }

        if option == "NONAPPROX":
            return {
                "sql": "(lower(" + field_name + ") NOT LIKE lower(%s)) ",
                "params":("%" + value + "%", )
            }
        
        return { "sql":"", "params":() }

