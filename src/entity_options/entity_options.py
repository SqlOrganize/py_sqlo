from ..config import UNDEFINED

class EntityOptions:

    def __init__(self, db, entity_name: str, prefix: str = "") -> None:
        self._db = db # Db
        self._entity_name: str = entity_name
        self._prefix: str = prefix

    def pf(self):
        """ prefijo fields
        """
        return  self._prefix + "-" if self._prefix  else ""

    def pt(self):
        """ prefijo table
        """
        return self._prefix if self._prefix else self._db.entity(self._entity_name).alias()
    
    def call_fields(self, field_names: list[str], method:str):
        """ Ejecutar metodo en fields
        """
        for field_name in field_names:
            getattr(self, method)(field_name)

        return self
    
    def call(self, method:str):
        """
        Ejecutar metodo en field_names definidos en la configuracion de la entidad

        Los metodos posibles para ejecucion no deben llevar otro parametro mas que el field_name
        """
        return self.call_fields(self._db.field_names(self._entity_name), method)
    
    def to_fields(self, field_names: list[str], method:str) -> dict: 
        """ 
        Ejecutar metodo y almacenar valores en un diccionario
        """
        row = {}
        for field_name in field_names:
            r = getattr(self, method)(field_name)
            if r != UNDEFINED:
                row[field_name] = r

        return row
    
    def to_(self, method:str) -> dict: 
        return self.to_fields(self._db.field_names(self._entity_name), method)


    def from_fields(self, row: dict, field_names: list[str], method:str) -> list: 
        """ 
        Ejecutar metodo y obtener valores desde un diccionario
        """
        if row:
            for field_name in field_names:
                if self.pf()+field_name in row:
                    getattr(self, method)(field_name, row[self.pf()+field_name])

        return self
        
    
    def from_(self, row: dict, method:str) -> list: 
        return self.from_fields(row, self._db.field_names(self._entity_name), method)


