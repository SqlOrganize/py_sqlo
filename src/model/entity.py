

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
        "no fk"
        return self._fields(self._nf)

    def mo(self):
        "many to one"
        return self._fields(self._mu)

    def oo(self):
        "one to one left"
        return self._fields(self.__u)

    def _fields(self, fieldNames):
        fields = []
        for fieldName in fieldNames:
            fields.append(Entity.container.field(self.name(), fieldName))
        return fields

    def fk(self):
        return self.mo() + self.oo()

    def fields(self):
        l = self.fieldsNoPk()
        l.insert(0, self.pk())
        return l
    

    def fieldsNoPk(self):
        return self.nf()+self.mo()+self.oo()


    def um():
        fields = []
        
    foreach($this->getStructure() as $entity){
      foreach($entity->getFieldsMu() as $field){
        if($field->getEntityRef()->getName() == $this->getName()){
          array_push($fields, $field);
        }
      }
    }
    return $fields;
  }


    def ref():
        return array_merge($this->getFieldsUm(), $this->getFieldsU_()); } //ref (um y u_)

    
    

    






