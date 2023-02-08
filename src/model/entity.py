

from icontainer import IContainer

class Entity:
    container: IContainer

    def __init__(self, config:dict) -> None:
        self._name = None
        self._alias = None
        self._schema = None
        
        self._nf = []
        self._mu = []
        self.__u = []
        self._identifier = None
        """ 
        array dinamico para identificar univocamente a una entidad en un momento determinado
        @example
        identifier = ["fecha_anio", "fecha_semestre","persona-numero_documento"]
        """

        self._orderDefault = []
        """
        Valores por defecto para ordenamiento
        @example ["field1"=>"asc","field2"=>"desc",...];
        """

        self._noAdmin = []
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
        @example ["field1","field2",...]
        """
    
        self._uniqueMultiple = []
        """
        Valores unicos
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

    def a_(self):  
        """ alias. """
        return self._alias

    def name(self):
        return self._name

    def alias(self):
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
        return self._fields(self._mu)

    def oo(self):
        "fields one to one (local fk)"
        return self._fields(self.__u)

    def _fields(self, fieldNames):
        fields = []
        for fieldName in fieldNames:
            fields.append(Entity.container.field(self.name(), fieldName))
        return fields

    def fk(self):
        "fields fk (mo and oo)"
        return self.mo() + self.oo()

    def fieldsNoPk(self):
        "all fields except pk"
        return self.nf()+self.mo()+self.oo()

    def fields(self):
        "all fields pk and fk (mo and oo)"
        l = self.fieldsNoPk()
        l.insert(0, self.pk())
        return l
    
    def om(self):
        """
        fields one to many
        its neccesary to iterate over all entities
        """
        fields = []
        for entityName in Entity.container.entityNames():
            e = Entity.container.entity(entityName)
            for f in e.mo():
                if f.entityRefName() == self.name():
                    fields.append(f)

        return fields

    def oo_(self):
        """
        fields one to one
        fk pointed to this entity
        its neccesary to iterate over all entities
        """
        fields = []
        for entityName in Entity.container.entityNames():
            e = Entity.container.entity(entityName)
            for f in e.oo():
                if f.entityRefName() == self.name():
                    fields.append(f)

        return fields

    def ref(self):
        return self.om()+self.oo()
    
    def orderDefault(self):
        return self._orderDefault

    def fieldNames(self)
        return Entity.container.fieldNames(self.name())

    
    






