


class Log():
    
    ERROR, WARNING, SUCCESS, INFO  = 2, 1, 0, -1

    def __init__(self, level=ERROR, msg="", type=None) -> None:
        self._level = level
        self._msg = msg
        self._type = type 

class Logging():
    """
    Clase simple para administrar logs de valores
    """

    LEVEL_ERROR, LEVEL_WARNING, LEVEL_INFO = 2, 1, 0

    def __init__(self) -> None:
        self._logs: dict[list[Log]] = {}
        """
        Cada elemento es tambien un diccionario con los campos "level", "type", "msg"
        Level puede tomar valores "error", "warning" o "info".
                   
        [
            "asignatura": {
                {"level": LEVEL_ERROR, "msg": "No puede estar vacío", type: "required"}
            }
            "plan": [
                {"level": LEVEL_WARNING, "msg: "No tiene cargas horarias asociadas", type: "user"}
            }
            "numero": {
                {"level": LEVEL_ERROR, "msg": "No es unico", type:"not_unique"}
                {"level": LEVEL_WARNING, "msg": "Esta fuera del rango permitido", type:"out_of_range"}
            }
        }
        """

        self._level:str = "info"
        """
        Nivel mas critico logeado hasta el momento
        
        Por defecto se asigna el menos critico "info"
        """
    
    def logs(self):
        return self._logs
    
    def logs_key(self, key):
        return self._logs[key] if key in self._logs else None
    
    def reset_logs(self, key):
        """ 
        Vaciar logs de una determinada llave

        Reasignar level
        """
        self._logs.pop(key, None)
        self._reset_level()
        return self

    def clear(self):
        """
        Vaciar todos los logs
        """
        self._logs = {}
        self._level = self.LEVEL_INFO
        return self
    
    def add_log(self, key: str, log: Log):
        """
        Agregar log a una determinada llave

        Los logs se ordenan de mayor a menor teniendo en cuenta el nivel
        """
        if not key in self._logs:
           self._logs[key] = []
        
        self._logs[key].append(log)

        self._logs[key] = sorted(self._logs[key], key=lambda d: d["level"], reverse=True)

    def level_key(self, key):
        if not key in self._logs:
            return None
        
        level = self.LEVEL_INFO
        for log in self._logs[key]:
            if level < log["level"]:
                level = log["level"]  
            
        return level