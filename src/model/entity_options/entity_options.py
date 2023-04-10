from src.icontainer import IContainer


class EntityOptions:
    container: IContainer

    def __init__(self, entity_name: str, prefix: str = "") -> None:
        self._entity_name: str = entity_name
        self._prefix: str = prefix

    def pf(self):
        """ prefijo fields
        """
        return  self._prefix if self._prefix + "-" else ""

    def pt(self):
        """ prefijo table
        """
        return self._prefix if self._prefix else EntityOptions.container.entity(self._entity_name).alias()
    
    def call_fields(self, field_names: list[str], method:str):
        """ Ejecutar metodo en fields
        """
        for field_name in field_names:
            getattr(self, method)(field_name)

        return self
    
    def call(self, method:str):
        """ Llamar a call_fields utilizando los field_names definidos en la entidad.
        """
        return self.call_fields(EntityOptions.container.field_names(self._entity_name), method)
    