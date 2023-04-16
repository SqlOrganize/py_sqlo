from py_sqlo.src.entity_options.entity_options import EntityOptions
from .mapping_i import MappingI
from ..config import UNDEFINED

class Mapping(EntityOptions):
    """ 
    Mapear campos para que sean entendidos por el motor de base de datos 
    
    Ejemplo de subclase opcional:

    -class ComisionMapping(Mapping):
        def numero(self):
           return '''
    CONCAT("+self.pf()+"sed.numero, "+self.pt()+".division)
'''
    """

    def map(self, field_name: str):
        """ 
        Verificar la existencia de metodo eclusivo, si no exite, buscar metodo
        predefinido.

        TODO: 
        -Permitir la aplicacion de varios mapping utilizando el caracter "." como
        separador
     
        Ejemplo: 
        -mapping.map("nombre")
        -mapping.map("fecha_alta.max.y"); //aplicar max, luego y
        -mapping.map("edad.avg")
        """
        m = field_name.replace(".", "_")
        if hasattr(self.__class__, m) and callable(getattr(self.__class__, m)):
            return getattr(self, m)()

        p = field_name.split(".")
        m = "_default" if len(p) == 1 else "_"+p[1]
        print("ejecutar "+m+ " "+p[0])
        #return getattr(self, m)(p[0])

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

        return 'CONCAT_WS("'+UNDEFINED+'",'+','.join(identifier)+''')
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
                self._recursive_label(field_id, subtree, fields_label)

        fields_label_ = []

        for l in fields_label:
            def res(f) -> str:
                f = Mapping.container.explode_field(self._entity_name, f)
                return Mapping.container.mapping(f["entity_name"], f["field_id"]).map(f["field_name"])
            fields_label_.append(res(l))

        return "CONCAT_WS(' ', "+",".join(fields_label_)+")"

    def _recursive_label(self, key: str, tree: dict, fields_label: list):
        """
        Se completa fields_label por referencia de forma recursiva
        """
        e = Mapping.container.entity(self._entity_name)

        for field in e.nf():
            if field.is_main():
                fields_label.append(key+"-"+field.name())

        for field_id, subtree in tree["children"]:
            if Mapping.container.field_by_id(e.name()).is_main():
                self._recursive_label(field_id, subtree, fields_label)

