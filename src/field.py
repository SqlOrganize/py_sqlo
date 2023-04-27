


class Field():
    def __init__(self, db, entity_name:str, field_name:str) -> None:
        self._db = db #Db
        self._name = field_name
        self._entity_name = entity_name
        self._entity_ref_name = None
        self._alias = None
        self._default = None
        """ puede ser false para booleanos """

        self._length = None
        """ longitud del field """

        self._max = None
        """ valor maximo """ 

        self._min = None
        """ valor minimo """ 

        self._type = None
        """ Tipo de datos generico 
            int
            blob
            string
            boolean
            float
            text
            timestamp
            date
        """ 

        self._fieldType = None
        """string con el tipo de field
            "pk": Clave primaria
            "nf": Field normal
            "mu": Clave foranea muchos a uno
            "_u": Clave foranea uno a uno
        """
        
        self._values = list()
        """
            lista de valores permitidos
        """
    
        config = self._db.field_config(entity_name, field_name)
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
    
    def name(self):
        """ name """
        return self._name
        
    def alias(self):  
        """ alias """
        return self._alias

    def entity(self):
        return self._db.entity(self._entity_name)

    def entity_ref(self):
        return self._db.entity(self._entity_ref_name)
    
    def is_main(self):
        return True if self.name() in self._db.entity(self._entity_name).main() else False

    def type(self):
        return self._type
    
    def default(self):
        return self._default


