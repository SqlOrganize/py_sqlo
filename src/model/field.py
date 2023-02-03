

from icontainer import IContainer

class Field:
    container: IContainer

    def __init__(self, config:dict) -> None:
        self.name = None
        self.entityName = None
        self.entityRefName = None
        self.alias = None
        self.default = None
        """ puede ser false para booleanos """

        self.length = None
        """ longitud del field """

        self.max = None
        """ valor maximo """ 

        self.min = None
        """ valor minimo """ 

        self.type = None
        """ tipo de datos definidos en la base de datos """ 

        self.dataType = "string"
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

        self.fieldType = None
        """string con el tipo de field
            "pk": Clave primaria
            "nf": Field normal
            "mu": Clave foranea muchos a uno
            "_u": Clave foranea uno a uno
        """
        
        self.values = list()
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

            setattr(self, k, config[k])

    def n_(self):
        """ name """
        return self.name
        
    def a_(self):  
        """ alias. """
        return self.alias
        




