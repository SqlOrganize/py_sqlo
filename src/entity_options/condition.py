from ..config import UNDEFINED
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

        p = field_name.split(".")
        if len(p) == 1:
           return self._define_condition_field(field_name)

        m = "_"+p.pop()
        return getattr(self, m)(".".join(p))

    def _define_condition_field(self, field_name):
        """
        traducir field_name sin funcion
        """
        field = self.__class__.container.field(self._entity_name, field_name)
        match field.data_type():
            case ["string" | "text"]:
                return "_string"

            case "boolean":
                return "_boolean"

            case other:
                return "_default"

    def label_search(self, option, value) -> str:
        """
        Combinacion entre label y search
        """
        cond1 =  self.cond("label",option, value)
        cond2 =  self.cond("search", option, value)
        return "(" + cond1 + "OR " + cond2 + ")"
 
  }