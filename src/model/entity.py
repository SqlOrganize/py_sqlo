

from icontainer import IContainer

class Entity:
    container: IContainer

    def __init__(self, config:dict) -> None:
        self.name = None
        self.alias = None
        self.schema = None
        
        self.nf = []
        self.mu = []
        self._u = []
        self.identifier = None
        """ 
        array dinamico para identificar univocamente a una entidad en un momento determinado
        @example
        identifier = ["fecha_anio", "fecha_semestre","persona-numero_documento"]
        """

        self.orderDefault = []
        """
        Valores por defecto para ordenamiento
        @example ["field1"=>"asc","field2"=>"desc",...];
        """

        self.noAdmin = []
        """
        Valores no administrables
        @example ["field1","field2",...]
        """

        self.main = ["id"]
        """
        Valores principales
        @example ["field1","field2",...]
        """

        self.unique = ["id"]
        """
        Valores unicos
        @example ["field1","field2",...]
        """
    
        self.uniqueMultiple = []
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

            setattr(self, k, config[k])

    def n_(self):
        """ name """
        return self.name
        
    def s_(self):
        """ schema. """
        return self.schema + "." if self.schema else "" 
     
    def sn_(self):
        """ schema.name """
        return self.s_() + self.n_() 

    def sna_(self):
        """ schema.name AS alias """
        return self.sn_() + " AS " + self.alias

    def a_(self):  
        """ alias. """
        return self.alias

    def getPk(self):
        return Entity.container.field(self.n_(), "id")





