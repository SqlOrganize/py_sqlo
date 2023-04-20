


class EntityTools():
    def __init__(self, db, entity_name) -> None:
        self._db = db
        self._entity_name = entity_name

    def field_names(self):
        "field_names from entity_name and its relations"
        field_namesR = []
        for fieldId, config in self._db.relations(self._entity_name).items():
            field_namesR += [fieldId+"-"+field_name for field_name in self._db.field_names(config["entity_name"])]

        return self._db.field_names(self._entity_name) + field_namesR

