

from icontainer import IContainer

class Field:
    container: IContainer

    def __init__(self, config:dict) -> None:
        self._name = None
        self._entityName = None
        self._entityRefName = None
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

        self._dataType = "string"
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

    def n_(self):
        """ name """
        return self._name
    
    def name(self):
        """ name """
        return self._name

    def a_(self):  
        """ alias. """
        return self._alias
        
    def alias(self):  
        """ alias. """
        return self._alias

    def entityName(self):
        return self._entityName

    def entityRefName(self):
        return self._entityRefName

    def entity(self):
        return Field.container.entity(self._entityName)

    def entityRef(self):
        return Field.container.entity(self._entityRefName)


