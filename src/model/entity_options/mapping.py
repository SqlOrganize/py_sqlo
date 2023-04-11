from src.config import UNDEFINED
from src.model.entity_options.entity_options import EntityOptions

class MappingEntityOptions(EntityOptions):
    """ Ejemplo redefinir
    class ComisionMapping(MappingEntityOptions):
        def numero(self):
           return '''
    CONCAT("+self.pf()+"sed.numero, "+self.pt()+".division)
'''
    """

    def count(self) -> str:
        return "COUNT(*)"
    
    def identifier(self):
        """ Concatenacion de campos que permiten identificar univocamente a la
        entidad. Pueden ser campos de relaciones.
        """
        e = MappingEntityOptions.container.entity(self._entity_name)
        if not e.identifier():
            raise "Identificador no definido en la entidad ". e.name()
            
        identifier = []
        for field_name in e.identifier():
            f = MappingEntityOptions.container.explode_field(self._entity_name, field_name)
            identifier.append(MappingEntityOptions.container.mapping(f["entity_name"], f["field_id"])).map(f["field_name"])

        return 'CONCAT_WS("'+UNDEFINED+'",'+','.join(identifier)+''')
'''

    def label(self):
        fields_label = []

        e = MappingEntityOptions.container.entity(self._entity_name)

        tree = MappingEntityOptions.container.tree(self._entity_name)

        for field in e.nf():
            if field.isMain():
                fields_label.append(field.name())

        for field_id, subtree in tree:
            if MappingEntityOptions.container.field_by_id(self._entity_name, field_id).isMain():
                self._recursive_label(field_id, subtree, fields_label)

        fields_label_ = []

        for l in fields_label:
            def res(f):
                f = MappingEntityOptions.container.explode_field(self._entity_name, f)
                return MappingEntityOptions.container.mapping(f["entity_name"], f["field_id"]).map(f["field_name"])
            fields_label_.append(res(l))

        return fields_label_


    def _recursive_label(self, key: str, tree: dict, fields_label: list):
        e = MappingEntityOptions.container.entity(self._entity_name)

        for field in e.nf():
            if field.is_main():
                fields_label.append(key+"-"+field.name())

        for field_id, subtree in tree["children"]:
            if MappingEntityOptions.container.field_by_id(e.name()).is_main():
                self._recursive_label(field_id, subtree, fields_label)
