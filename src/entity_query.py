
from .config import AND_, APPROX, EQUAL, FF, NONAPPROX, OR_, NONEQUAL
from .function.add_prefix_multi_list import add_prefix_multi_list
from .function.add_prefix_dict import add_prefix_dict
from .function.remove_prefix_multi_list import remove_prefix_multi_list
from .function.remove_prefix_dict import remove_prefix_dict
from abc import abstractmethod


class EntityQuery:
    def __init__(self, db, entity_name:str) -> None:
        self._db = db
        self._entity_name = entity_name
        self._condition = tuple()
        """
        condicion
        array multiple cuya raiz es [field,option,value], ejemplo: [["nombre","=","unNombre"],[["apellido","=","unApellido"],["apellido","=","otroApellido","OR"]]]
        """
                
        self._order = {}
        self._page = 1
        self._size = 100
        self._fields = []
        """
        Deben estar definidos en el mapping field, se realizará la traducción 
        correspondiente
        . indica aplicacion de funcion de agregacion
        - indica que pertenece a una relacion
        Ej ["nombres", "horas_catedra.sum", "edad.avg", "com_cur-horas_catedra]
        """
        self._fields_concat = {}
        """
        Similar a _fields pero se define un alias para concatenar un conjunto de fields
        Ej ["nombre" => ["nombres", "apellidos"], "max" => ["horas_catedra.max", "edad.max"]]
        """
        self._group = []      
        """
        Similar a fields pero campo de agrupamiento
        """
        self._group_concat = {}      
        """
        Similar a _fields_concat pero campo de agrupamiento
        """
        self._having = []
        """
        condicion de agrupamiento
        array multiple cuya raiz es [field,option,value], ejemplo: [["nombre","=","unNombre"],[["apellido","=","unApellido"],["apellido","=","otroApellido","OR"]]]
        """

        self._str_agg: dict = {}
        """
        Campos a los cuales se aplica str_agg

        Array multiple definido por alias y los campos que se aplica str_agg

        @EXAMPLE

        -{"alias" => ["field1","field2"]} 
        
        @TRADUCCION DEL EJEMPLO

        -GROUP_CONCAT(DISTINCT field1_map, " ", field2_map) AS "alias"

        @STR_AGG A UN SOLO VALOR

        Para aplicar GROUP_CONCAT a un solo valor, se puede utilizar como al-
        ternativa la funcion de agreacion, por ejemplo persona.str_agg que se
        traduce a:        
        
        -GROUP_CONCAT(DISTINCT persona)
        """

    def cond(self, condition:tuple):
        self._condition = self._condition + condition
        return self

    def param(self, key:str, value): 
        return self.cond([key, "=",value])

    def params(self, params:dict):
        for k,v in params.items():
            self.cond([k,"=",v])
        return self

    def order (self, order:dict):
        self._order = order
        return self
    
    def size(self, size):
        self._size = size
        return self
    
    def page(self, page):
        self._page = page
        return self

    def field(self, field: str):
        self._fields.append(field)
        return self

    def fields(self, fields: list[str] = None):
        if not fields:
            return self.fields_tree()
        
        self._fields = list(set(self._fields + fields))
        return self

    def fields_tree(self):
        self._fields = self._db.tools(self._entity_name).field_names()
        return self

    def fields_concat(self, fields: dict[list[str]]):
        self._fields_concat.update(fields)
        return self

    def group(self, group: list[str]):
        self._group = list(set(self._group + group))
        return self

    def group_concat(self, group: dict[list[str]]):
        self._group_concat.update(group)
        return self
    
    def str_agg(self, fields: dict[list[str]]):
        self._str_agg.update(fields)
        return self

    def hav(self, having: list):
        self._having.append(having)
        return self

    def _add_prefix(self, prefix: str):
        self._condition = add_prefix_multi_list(self._condition, prefix)
        self._order = add_prefix_dict(self._order, prefix)
        return self

    def _remove_prefix(self, prefix: str):
        self._condition = remove_prefix_multi_list(self._condition, prefix)
        self._order = remove_prefix_dict(self._order, prefix)
        return self

    def unique(self, params:dict):
        """ definir condicion para campos unicos 
        # ejemplo params
        {"field_name":"field_value", ...}
        
        # campos unicos simples
        Se definen a traves del atributo Entity._unique

        # campos unicos multiples
        Se definen a traves del atributo Entity._unique_multiple
        """
        unique_fields: list = self._db.entity(self._entity_name).unique()
        unique_fields_multiple: list = self._db.entity(self._entity_name).unique_multiple()
        
        condition = []
        # if "id" in params and params["id"]:
        #     condition.append(["id", EQUAL, params["id"]])

        first = True 
        
        for f in unique_fields:
            for k, v in params.items():
                if k == f and v:
                    if first:
                        con = AND_
                        first = False
                    else:
                        con = OR_    

                    condition.append([k, EQUAL, v, con])
        
        if unique_fields_multiple:
            condition_multiple = []
            first = True 
            exists_condition_multiple = True #si algun campo de la condicion multiple no se encuentra definido, se carga en True.
            for f in unique_fields_multiple:
                if not exists_condition_multiple:
                    break

                exists_condition_multiple = False

                for k, v in params.items():
                    if k == f:
                        exists_condition_multiple = True
                        if first and condition:
                            con = OR_
                            first = False
                        else:
                            con = AND_    

                        condition_multiple.append([k, EQUAL, v, con])

            if exists_condition_multiple and condition_multiple:
                condition.append(condition_multiple)

        if not condition:
            raise "Error al definir condition unica"

        self.cond(condition)

        return self

    @abstractmethod
    def build(self) -> dict:
        """
        Construir SQL

        El sql debe ser invocado al finalizar todas las asignaciones de atributos.
        Posponer la construccion del SQL permite que sea mas flexible la invocacion de parametros
        La asignacion de atributos puede hacerse en cualquier orden
        """
        pass


