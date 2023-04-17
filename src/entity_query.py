
from .config import AND_, EQUAL, OR_
from .function.add_prefix_multi_list import add_prefix_multi_list
from .function.add_prefix_dict import add_prefix_dict
from .function.remove_prefix_multi_list import remove_prefix_multi_list
from .function.remove_prefix_dict import remove_prefix_dict

class EntityQuery:
    container: any #Container

    def __init__(self, entity_name) -> None:
        self._entity_name = entity_name
        self._condition = []
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

    def cond (self, condition:list):
        self._condition.append(condition)
        return self

    def param (self, key:str, value): 
        return self.cond([key, "=",value])

    def params (self, params:dict):
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
        self._fields = EntityQuery.container.tools(self._entity_name).field_names()
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

    def having(self, having: list):
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
        unique_fields: list = EntityQuery.container.entity(self._entity_name).unique()
        unique_fields_multiple: list = EntityQuery.container.entity(self._entity_name).unique_multiple()
        
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

    def _sql_fields(self) -> str:
        """
        SQL FIELDS
        """
        field_names = list(set(self._group + self._fields))

        sql_fields = []

        for field_name in field_names:
            ff = EntityQuery.container.explode_field(self._entity_name, field_name)
            map = EntityQuery.container.mapping(ff["entity_name"], ff["field_id"]).map(ff["field_name"])
            # $prefix = (!empty($f["field_id"])) ? $f["field_id"] . "-" : "";
            # $alias = (is_integer($key)) ? $prefix . $f["field_name"] : $key;
            # $f = $map . " AS \"" . $alias . "\"";

        return ""
    
    def sql(self) -> str:
        sql_fields = self._sql_fields()
        
        sql = """ SELECT DISTINCT
""" 
        sql += sql_fields
        return sql



