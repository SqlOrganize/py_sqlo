from py_sqlo.src.function.concat import concat
from ..entity_query import EntityQuery
from .options import OPTIONS


class EntityQueryMysql(EntityQuery):

    def sql(self) -> dict:
        cond = self._sql_cond(self._condition)
        hav = self._sql_cond(self._having)
#         having = h[0]
#         v = c[1] + h[1]

#         sql = """ SELECT DISTINCT
# """ + self._sql_fields() + """
# """ + self._sql_from() + """
# """ + self._join() + """
# """ + concat(condition, 'WHERE ') + """
# """ + self._group_by() + """
# """ + concat(having, 'WHERE ')

#         return {"sql":sql, "params":v}

    def _sql_fields(self) -> str:
        """
        SQL FIELDS
        """
        sql_fields = []

        """
        procesar _group y _fields
        """
        field_names = list(set(self._group + self._fields))
        field_names.sort()

        for field_name in field_names:
            ff = self._db.explode_field(self._entity_name, field_name)
            map = self._db.mapping(ff["entity_name"], ff["field_id"]).map(ff["field_name"])
            prefix = ff["field_id"]+"-" if ff["field_id"] else ""
            sql_fields.append(map+" AS \"" + prefix + ff["field_name"] + "\"")

        """
        procesar _group_concat y _fields_concat
        """
        field_names_concat = self._group_concat | self._fields_concat
        field_names_concat = dict(sorted(field_names_concat.items(), key=lambda item: item[1]))

        for alias, field_names in field_names_concat.items():
            map_ = []
            for field_name in field_names:
                ff = self._db.explode_field(self._entity_name, field_name)
                map = self._db.mapping(ff["entity_name"], ff["field_id"]).map(ff["field_name"])
                map_.append(map)
            sql_fields.append("CONCAT_WS(', ', " + ", ".join(map_) + ") AS " + alias)

        """
        procesar _str_agg
        """
        _str_agg = dict(sorted(self._str_agg.items(), key=lambda item: item[1]))

        for alias, field_names in _str_agg.items():
            map_ = []
            for field_name in field_names:
                ff = self._db.explode_field(self._entity_name, field_name)
                map = self._db.mapping(ff["entity_name"], ff["field_id"]).map(ff["field_name"])
                map_.append(map)
            sql_fields.append("GROUP_CONCAT(DISTINCT " + ", ' ', ".join(map_) + ") AS " + alias)

        return """,
""".join(sql_fields) 
    
    def _group_by(self) -> str:
        if not self._group and not self._group_concat:
            return ""
        
        group = []
        for field_name in self._group:
            f = self._db.explode_field(self._entity_name, field_name)
            map = self._db.mapping(f["entity_name"], f["field_id"]).map(f["field_name"])
            group.append(map)

        for alias, field_name in self._group_concat.items():
            group.append(alias)

        return "GROUP BY "+", ".join(group)+"""
"""
    
    def _sql_from(self) -> str:    
        return """ FROM 
""" + self._db.entity(self._entity_name).schema_name_alias() + """
"""

    def _join(self) -> str:
        tree = self._db.tree(self._entity_name)
        return self._join_fk(tree, "")


    def _join_fk(self, tree: dict, table_prefix: str):
        sql = ""

        if not table_prefix:
            table_prefix = self._db.entity(self._entity_name).alias()

        for field_id, value in tree.items():
            entity_sn = self._db.entity(value["entity_name"]).schema_name()
            sql += "LEFT OUTER JOIN " + entity_sn + " AS " + field_id + " ON (" + table_prefix + "." + value["field_name"] + " = " + field_id + """.id)
"""
            if value["children"]:
                sql += self._join_fk(value["children"], field_id)

        return sql

    def _sql_cond(self, condition:tuple):
        """
        Metodo inicial para definir condicion
        """
        if not condition:
            return ("",())
        
        condition_conc = self._sql_cond_recursive(condition)
        return condition_conc

    def _sql_cond_recursive(self, condition: tuple) -> dict:
        """
        Metodo recursivo para definir condicion

        Si en la posicion 0 es un string significa que es un campo a buscar, 
        caso contrario es una nueva tupla

        Return tuple, example:
        {
            "sql": "nombres LIKE %s"
            "params": ("valores de variables",)
            "con": "AND"
        }
        """

        if isinstance(condition[0], tuple):
            return self._sql_cond_iterable(condition)
        
        if not condition and not isinstance(condition[0], str):
            raise "Error en el campo de la condicion"

        try:
            option = condition[1]
        except IndexError:
            option = "EQUAL"

        try:
            value = condition[2]
        except IndexError:
            value = None #hay opciones de configuracion que pueden no definir valores

        try:
            con = condition[3]
        except IndexError:
            con = "AND" #el modo indica la concatenacion con la opcion precedente

        condition_ = self._sql_cond_field_check_value(condition[0], option, value)
        condition_["con"] = con #se agrega el conector
        return condition_
    
    def _sql_cond_iterable(self, condition_iterable: tuple) -> dict:
        """
        Metodo iterable para definir condicion

        Si  la posicion 0 de condition_iterable es un string significa que es un campo a buscar

        Return tuple, example:
        {
            "sql": "nombres LIKE %s"
            "params": ("valores de variables",)
            "con": "AND"
        }
        """
    
        conditions_conc = tuple()
        """
        Tupla de dict
        ({"sql":..., "params":..., "con":...}, {"sql":..., "params":..., "con":...}, ...)
        """


        for ci in condition_iterable:
            cc = self._sql_cond_recursive(ci)
            conditions_conc = conditions_conc + (cc, )
       
        ret = {
            "sql": "",
            "params": (),
        }

        for cc in conditions_conc:
            if ret["sql"]:
                ret["sql"] += """
""" + cc["con"] + " "

            ret["sql"] += cc["sql"]
            ret["params"] = ret["params"] + cc["params"]
            
        return {
            "sql": """(
""" + ret["sql"] + """
)""", 
            "params":ret["params"],
            "con": conditions_conc[0]["con"] #primera condicion de la iteracion
        }

    def _sql_cond_field_check_value(self, field: str, option, value) -> dict:
        """
        Combinar parametros y definir SQL
        """
        if not isinstance(value, tuple):
            condition = self._sql_cond_field(field, option, value)
            if not condition:
                 raise "No pudo definirse el SQL de la condicion del campo: " + self._entity_name + "." + field
            return condition

        condition = {
            "sql":"",
            "params":()
        }
        cond = False #flag para indicar que debe imprimirse condicion

        for v in value:
            if cond:
                sql = " {} ".format(OPTIONS["OR"]) if option == "EQUAL" or option == "APPROX" else " {} ".format(OPTIONS["AND"]) if option == "NONEQUAL" or option == "NONAPPROX" else False
                if not sql:
                    raise "Error al definir opción para " + field + " " + option + " " + value
                condition["sql"] += sql

            else:
                cond = True 

            condition_ = self._sql_cond_field_check_value(field, option, v)
            condition["sql"] += condition_["sql"]
            condition["params"] = condition["params"] + condition_["params"]

        return {
            "sql":"""(
""" + condition["sql"] + """
)""",
            "params":condition["params"]
        }

    def _sql_cond_field(self, field, option, value: str) -> dict:
        """
        Traducir campo y definir SQL con la opcion

        Return:
        -("str with condition", ("tuple with vars"))
        """
        f = self._db.explode_field(self._entity_name, field)

        if isinstance(value, str) and value[0].startswith("$"): #definir condicion entre fields
            v = self._db.explode_field(self._entity_name, value[0].replace("$", '', 1))
            field_sql1 = self._db.mapping(f["entity_name"], f["field_id"]).map(f["field_name"])
            field_sql2 = self._db.mapping(v["entity_name"], v["field_id"]).map(v["field_name"])

            if option == "APPROX":
                return {
                    "sql":"(lower(CAST(" + field_sql1 + " AS CHAR)) LIKE CONCAT('%', lower(CAST(" + field_sql2 + " AS CHAR)), '%'))",
                    "params":()
                }
            elif option == "NONAPPROX":
                return {
                    "sql":"(lower(CAST(" + field_sql1 + " AS CHAR)) NOT LIKE CONCAT('%', lower(CAST(" + field_sql2 + " AS CHAR)), '%'))",
                    "params":()
                }
            else:
                {
                    "sql":"(" + field_sql1 + " " + option + " " + field_sql2 + ") ",
                    "params":()
                }
    
        return self._db.condition(f["entity_name"], f["field_id"]).cond(f["field_name"], option, value)


