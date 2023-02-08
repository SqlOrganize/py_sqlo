

from icontainer import IContainer

class EntityTools:
    container: IContainer

    def __init__(self, entityName) -> None:
        self._entityName = entityName

    def fieldNames(self):
        EntityTools.container.entity(self._entityName).getFieldNames()
        for key, value in EntityTools.container.relations(self._entityName):
