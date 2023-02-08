

from icontainer import IContainer

class EntityTools:
    container: IContainer

    def __init__(self, entityName) -> None:
        self._entityName = entityName

    def fieldNames(self):
        "fieldNames from entityName and its relations"
        for fieldId, config in EntityTools.container.relations(self._entityName):
            fieldNamesR = [fieldId+"-"+fieldName for fieldName in EntityTools.container.fieldNames(config["entity_name"])]

        return EntityTools.container.fieldNames(self._entityName) + fieldNamesR

