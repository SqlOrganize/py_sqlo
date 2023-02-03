

from icontainer import IContainer

class EntityQuery:
    container: IContainer

    def __init__(self, entityName) -> None:
        self.entityName = entityName
        self.condition = []
        """
        condicion
        array multiple cuya raiz es [field,option,value], ejemplo: [["nombre","=","unNombre"],[["apellido","=","unApellido"],["apellido","=","otroApellido","OR"]]]
        """
        
        self.order = []
        self.page = 1
        self.size = 100
        self.fields = []
        """
        Deben estar definidos en el mapping field, se realizará la traducción 
        correspondiente
        . indica aplicacion de funcion de agregacion
        - indica que pertenece a una relacion
        Ej ["nombres", "horas_catedra.sum", "edad.avg", "com_cur-horas_catedra]
        """

        self.group = []      
        self.having = []
        """
        condicion de agrupamiento
        array multiple cuya raiz es [field,option,value], ejemplo: [["nombre","=","unNombre"],[["apellido","=","unApellido"],["apellido","=","otroApellido","OR"]]]
        """

    def cond(self, condition):
        self.condition.append(condition)
        return self

    def param(self, key, value): 
        return self.cond([key, "=",value])
  


