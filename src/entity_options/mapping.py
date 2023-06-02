from ..config import UNDEFINED
from .entity_options import EntityOptions

class Mapping(EntityOptions):
    """
    Mapear campos para que sean entendidos por el motor de base de datos.

    Define SQL, cada motor debe tener su propia clase mapping de forma tal que
    sea traducido de forma correcta.

    Sintaxis MySQL, MariaDB.
    
    Ejemplo de subclase opcional:

    -class ComisionMapping(Mapping):
        def numero(self):
           return '''
    CONCAT("+self.pf()+"sed.numero, "+self.pt()+".division)
'''

    Las subclases deben soportar la sintaxis del motor que se encuentran 
    utilizando.
    """

    def map(self, field_name: str):
        """ 
        Verificar la existencia de metodo eclusivo, si no exite, buscar metodo
        predefinido.

        Ejemplo: 
        -mapping.map("nombre")
        -mapping.map("fecha_alta.max.y"); //aplicar max, luego y
        -mapping.map("edad.avg")
        """
        m = field_name.replace(".", "_")
        if hasattr(self.__class__, m) and callable(getattr(self.__class__, m)):
            return getattr(self, m)()

        p = field_name.split(".")
        if len(p) == 1:
           return _default(field_name)

        m = "_"+p.pop() #se comienza por la funcion ubicada mas a la derecha que sera la ultima en ejecutarse
        return getattr(self, m)(".".join(p))

    def count(self) -> str:
        return "COUNT(*)"
    
    def identifier(self):
        """ Concatenacion de campos que permiten identificar univocamente a la
        entidad. Pueden ser campos de relaciones.
        """
        e = Mapping.container.entity(self._entity_name)
        if not e.identifier():
            raise "Identificador no definido en la entidad ". e.name()
            
        identifier = []
        for field_name in e.identifier():
            f = Mapping.container.explode_field(self._entity_name, field_name)
            identifier.append(Mapping.container.mapping(f["entity_name"], f["field_id"])).map(f["field_name"])

        return 'CONCAT_WS("'+UNDEFINED+'",'+', '.join(identifier)+''')
'''

    def label(self) -> str:
        fields_label = []
        e = Mapping.container.entity(self._entity_name)
        tree = Mapping.container.tree(self._entity_name)

        for field in e.nf():
            if field.is_main():
                fields_label.append(field.name())

        for field_id, subtree in tree.items():
            if Mapping.container.field_by_id(self._entity_name, field_id).is_main():
                fields_label = fields_label + self._recursive_label(field_id, subtree)

        fields_label_ = []

        for l in fields_label:
            def res(f) -> str:
                f = Mapping.container.explode_field(self._entity_name, f)
                return Mapping.container.mapping(f["entity_name"], f["field_id"]).map(f["field_name"])
            fields_label_.append(res(l))

        return "CONCAT_WS(' ', "+", ".join(fields_label_)+")"

    def _recursive_label(self, key: str, tree: dict):
        """
        Se completa fields_label por referencia de forma recursiva
        """
        fields_label: list = []

        e = Mapping.container.entity(tree["entity_name"])

        for field in e.nf():
            if field.is_main():
                fields_label.append(key+"-"+field.name())

        for field_id, subtree in tree["children"].items():
            if Mapping.container.field_by_id(e.name(), field_id).is_main():
                fields_label = fields_label + self._recursive_label(field_id, subtree)

        return fields_label

    def search(self) -> str:
        fields_search = []
        for f in self.__class__.container.entity(self._entity_name).nf():
            fields_search.append(self.__class__.container.mapping(self._entity_name, self._prefix).map(f.name()))

        return "CONCAT_WS(' ', "+", ".join(fields_search)+")"

    def _default(self, field: str) -> str:
        return self.pt()+"."+field
    
    def _date(self, field: str) -> str: 
        return "CAST("+self.map(field)+" AS DATE)"
    
    def _ym(self, field: str) -> str: 
        return "DATE_FORMAT("+self.map(field)+", '%Y-%m')"
    
    def _y(self, field: str) -> str: 
        return "DATE_FORMAT("+self.map(field)+", '%Y')"
    
    def _avg(self, field: str) -> str: 
        return "AVG("+self.map(field)+")"
    
    def _min(self, field: str) -> str: 
        return "MIN("+self.map(field)+")"
    
    def _max(self, field: str) -> str:
        return "MAX("+self.map(field)+")"
    
    def _sum(self, field: str) -> str: 
        return "SUM("+self.map(field)+")"
    
    def _count(self, field: str) -> str: 
        return "COUNT(DISTINCT "+self.map(field)+")"
    
    def _exists(self, field: str) -> str: 
        return self._default(field)
    
    def _str_agg(self, field: str) -> str: 
        return "GROUP_CONCAT(DISTINCT "+self.map(field)+" SEPARATOR ', ')"

