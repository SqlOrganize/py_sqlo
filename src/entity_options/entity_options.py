from ..config import UNDEFINED

class EntityOptions:
    container: any #Container

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
    
    def to_fields(self, field_names: list[str], method:str) -> dict: 
        """ Ejecutar metodo y almacenar resultado en n array de fields
        """
        row = {}
        for field_name in field_names:
            r = getattr(self, method)(field_name)
            if r != UNDEFINED:
                row[field_name] = r

        return row
    
    def to_(self, method:str) -> dict: 
        return self.to_fields(EntityOptions.container.field_names(self._entity_name), method)


    def from_fields(self, row: dict, field_names: list[str], method:str) -> list: 
        """ Ejecutar metodo y almacenar resultado en n array de fields
        """
        if row:
            for field_name in field_names:
                if self.pf()+field_name in row:
                    getattr(self, method)(field_name, row[self.pf()+field_name])

        return self
        
    
    def from_(self, row: dict, method:str) -> list: 
        return self.from_fields(row, EntityOptions.container.field_names(self._entity_name), method)


