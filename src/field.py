


class Field():
    container: any #Container

    def __init__(self, db, config:dict) -> None:
        self.db = db #Database
        self._name = None
        self._entity_name = None
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
        """ tipo de datos definidos en la base de datos """ 

        self._data_type = "string"
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
        return Field.container.entity(self._entity_name)

    def entity_ref(self):
        return Field.container.entity(self._entity_ref_name)
    
    def is_main(self):
        return True if self.name() in Field.container.entity(self._entity_name).main() else False

    def data_type(self):
        return self._data_type
    


