from ..entity_query import EntityQuery
from .options import OPTIONS


class EntityQueryMysql(EntityQuery):
    def _condition_field(self, field, option, value: str) -> dict:
        """
        Traducir campo y definir SQL con la opcion

        Return:
        -("str with condition", ("tuple with vars"))
        """
        f = self._db.explode_field(self._entity_name, field)

        if value[0].startswith("$"): #definir condicion entre fields
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
                return ("(" + field_sql1 + " " + option + " " + field_sql2 + ") ",());  
    
        return self._db.condition(f["entity_name"], f["field_id"]).cond(f["field_name"], option, value)

