


class Entity():
    container: any #Container

    def __init__(self, db, entity_name:str) -> None:
        self.db = db #Database 
        self._name: str = entity_name
        self._alias: str = None
        self._schema: str = None
        
        self._nf: list[str] = []
        self._mo: list[str] = []
        self._oo: str = []
        self._identifier: list[str] = None
        """ 
        array dinamico para identificar univocamente a una entidad en un momento determinado
        @example
        identifier = ["fecha_anio", "fecha_semestre","persona-numero_documento"]
        """

        self._order_default: dict[str, str] = []
        """
        Valores por defecto para ordenamiento
        @example ["field1"=>"asc","field2"=>"desc",...];
        """

        self._no_admin: list[str] = []
        """
        Valores no administrables
        @example ["field1","field2",...]
        """

        self._main: list[str] = ["id"]
        """
        Valores principales
        @example ["field1","field2",...]
        """

        self._unique: list[str] = ["id"]
        """
        Valores unicos
        Una entidad puede tener varios campos que determinen un valor unico
        @example ["field1","field2",...]
        """
    
        self._unique_multiple: list[str] = []
        """
        Valores unicos
        Una entidad puede tener un y solo un conjunto de campos unique_multiple
        @example ["field1","field2",...]
        """
        config = db.entities_config(self.name())
        for k,v in config:
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

    def name(self) -> str:
        return self._name

    def alias(self) -> str:
        return self._alias
    
    def schema_(self):
        return self._schema + "." if self._schema else "" 
    
    def schema(self):
        return self._schema
    
    def schema_name(self):
        """ schema.name """
        return self.schema_() + self.name()
    
    def schema_name_alias(self):
        """ schema.name AS alias """
        return self.schema_name() + " AS " +  self.alias()

    def identifier(self) -> list[str]:
        return self._identifier

    def pk(self):
        "primary key"
        return Entity.container.field(self.name(), "id")

    def nf(self) -> list:
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
                if f.entity_ref().name() == self.name():
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
                if f.entity_ref().name() == self.name():
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
    
    def main(self) -> list[str]:
        return self._main


    






