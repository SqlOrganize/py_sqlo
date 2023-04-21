

import re
from ..config import UNDEFINED

class Validation():
    """
    Clase simple para verificar valores

    No se validan archivos
    """

    def __init__(self, value: any) -> None:
        self._value: any = value
        """
        Valor a verificar
        """

        self._errors: list[dict] = []
        """
        Errores de la verificacion
        Cada elemento de la lista es un diccionario con dos valores
        {
            type:"nombre de la funcion que genero el error".
            msg:"mensaje de error"
        }
        """

        self._level:str = "info"
        """
        Nivel mas critico logeado hasta el momento
        
        Por defecto se asigna el menos critico "info"
        """
    
    def _is_none_or_undefined(self):
        self.__class__.is_none_or_undefined(self._value)

        
    def _is_undefined(self):
        self.__class__.is_undefined(self._value)

    
    def name(self):
        if self.is_none_or_undefined():
            return self
        
        pattern = re.compile("/[^a-zA-ZáéíóúñÁÉÍÓÚÑçÇüÜ\s\']/")
        if not pattern.match(self._value):
            self._errors.append({"type":"name", "msg":"Formato no valido"})

    def required(self):
        if not self._is_none_or_undefined():
            self._errors.append({"type":"required", "msg":"Valor obligatorio"})

        return self

    @classmethod
    def is_none_or_undefined(cls, value):
        return True if cls.is_none(value) or cls.is_undefined(value) else False
    
    @classmethod
    def is_undefined(cls, value):
        return True if value == UNDEFINED else False
    
    @classmethod
    def is_none(cls, value):
        return True if value is None else False