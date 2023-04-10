

from src.icontainer import IContainer
from src.model.ientity import IEntity

class Entity(IEntity):
    container: IContainer

    def __init__(self, config:dict) -> None:
        self._name = None
        self._alias = None
        self._schema = None
        
        self._nf = []
        self._mo = []
        self._oo = []
        self._identifier = None
        """ 
        array dinamico para identificar univocamente a una entidad en un momento determinado
        @example
        identifier = ["fecha_anio", "fecha_semestre","persona-numero_documento"]
        """

        self._order_default = []
        """
        Valores por defecto para ordenamiento
        @example ["field1"=>"asc","field2"=>"desc",...];
        """

        self._no_admin = []
        """
        Valores no administrables
        @example ["field1","field2",...]
        """

        self._main = ["id"]
        """
        Valores principales
        @example ["field1","field2",...]
        """

        self._unique = ["id"]
        """
        Valores unicos
        Una entidad puede tener varios campos que determinen un valor unico
        @example ["field1","field2",...]
        """
    
        self._unique_multiple = []
        """
        Valores unicos
        Una entidad puede tener un y solo un conjunto de campos unique_multiple
        @example ["field1","field2",...]
        """
        for k,v in config.items():
            if "+" in k:
                k = k.rstrip("+")
                for vv in v:
                    if vv not in config[k]:
                        config[k].append(vv)
            elif "-" in k:
                k = k.rstrip("-")
                diff = [i for i in config[k] + v if i not in config[k] or i not in v]
                config[k] = diff

            setattr(self, "_"+k, config[k])

    def n_(self):
        """ name """
        return self._name
        
    def s_(self):
        """ schema. """
        return self._schema + "." if self._schema else "" 
     
    def sn_(self):
        """ schema.name """
        return self.s_() + self.n_() 

    def sna_(self):
        """ schema.name AS alias """
        return self.sn_() + " AS " + self._alias

    def a_(self) -> str:  
        """ alias. """
        return self._alias

    def name(self) -> str:
        return self._name

    def alias(self) -> str:
        return self._alias
    
    def schema(self):
        return self._schema

    def identifier(self):
        return self._identifier

    def pk(self):
        "primary key"
        return Entity.container.field(self.name(), "id")

    def nf(self):
        "fields no fk"
        return self._fields(self._nf)

    def mo(self):
        "fields many to one"
        return self._fields(self._mo)

    def oo(self):
        "fields one to one (local fk)"
        return self._fields(self._oo)

    def _fields(self, field_names):
        fields = []
        for field_name in field_names:
            fields.append(Entity.container.field(self.name(), field_name))
        return fields

    def fk(self):
        "fields fk (mo and oo)"
        return self.mo() + self.oo()

    def fields_no_pk(self):
        "all fields except pk"
        return self.nf()+self.mo()+self.oo()

    def fields(self):
        "all fields pk and fk (mo and oo)"
        l = self.fields_no_pk()
        l.insert(0, self.pk())
        return l
    
    def om(self):
        """
        fields one to many
        its neccesary to iterate over all entities
        """
        fields = []
        for entity_name in Entity.container.entity_names():
            e = Entity.container.entity(entity_name)
            for f in e.mo():
                if f.entity_ref_name() == self.name():
                    fields.append(f)

        return fields

    def oon(self):
        """
        fields one to one without local fk
        fk pointed to entity outside
        its neccesary to iterate over all entities
        """
        fields = []
        for entity_name in Entity.container.entity_names():
            e = Entity.container.entity(entity_name)
            for f in e.oo():
                if f.entity_ref_name() == self.name():
                    fields.append(f)

        return fields

    def ref(self):
        return self.om()+self.oo()
    
    def order_default(self):
        return self._order_default

    def field_names(self):
        return Entity.container.field_names(self.name())

    def unique(self) -> list:
        return self._unique

    def unique_multiple(self) -> list:
        return self._unique_multiple


    






