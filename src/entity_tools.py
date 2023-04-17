


class EntityTools():
    container: any #Container

    def __init__(self, entity_name) -> None:
        self._entity_name = entity_name

    def field_names(self):
        "field_names from entity_name and its relations"
        field_namesR = []
        for fieldId, config in EntityTools.container.relations(self._entity_name).items():
            field_namesR += [fieldId+"-"+field_name for field_name in EntityTools.container.field_names(config["entity_name"])]

        return EntityTools.container.field_names(self._entity_name) + field_namesR

