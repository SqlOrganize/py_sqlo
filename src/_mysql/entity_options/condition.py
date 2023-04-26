from ...function.to_bool import to_bool
from ..entity_options.condition import Condition
from ..options import OPTIONS

class ConditionMysql(Condition):

    def _define_condition(self, field_name):
        p = field_name.split(".")
        if len(p) == 1:
            field = self._db.field(self._entity_name, field_name)
            match field.data_type():
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
        if c:
            return c

        c = self._approx_cast(field, opt, value)
        if c:
            return c

        return {
            "sql":"(" + field + " " + OPTIONS[opt] + " %s) ",
            "params":self._value(field_name, value)
        }
    
    def _str(self, field_name, opt, value) -> tuple:
        field = self._db.mapping(self._entity_name, self._prefix).map(field_name)

        c = self._exists(field, opt, value)
        if c:
            return c

        c = self._approx(field, opt, value)
        if c:
            return c
        
        return {
            "sql":"(" + field + " " + OPTIONS[opt] + " %s) ",
            "params":self._value(field_name, value)
        }
    
    def _bool(self, field_name, option, value): 
        field = self._db.mapping(self._entity_name, self._prefix).map(field_name)

        return {
            "sql":"(" + field + " " + OPTIONS[option] + " %s) ",
            "params":self._value(field_name, value)
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
                "sql":"(CAST(" + field_name + " AS CHAR) LIKE %s) ",
                "params":("%" + value + "%")
            }

        if option == "NONAPPROX":
            return {
                "sql":"(CAST(" + field_name + " AS CHAR) NOT LIKE %s) ",
                "params":("%" + value + "%")
            }

        return { "sql":"", "params":() }

    def _approx(self, field_name, option, value) -> tuple:
        if option == "APPROX": 
            return {
                "sql":"(lower(" + field_name + ") LIKE lower(%s)) ",
                "params":("%" + value + "%",)
            }

        if option == "NONAPPROX":
            return {
                "sql": "(lower(" + field_name + ") NOT LIKE lower(%s)) ",
                "params":("%" + value + "%",)
            }
