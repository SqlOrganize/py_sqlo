import importlib
import mysql.connector
from mysql.connector.connection import MySQLConnection
import json
from os.path import exists

from py_sqlo.src.entity_options.entity_options import EntityOptions
from py_sqlo.src.entity_options.values import Values
from .function.snake_case_to_camel_case import snake_case_to_camel_case

from .entity import Entity
from .entity_options.mapping import Mapping
from .entity_options.condition import Condition
from .entity_query import EntityQuery
from .entity_tools import EntityTools
from .field import Field

class Db():
    """ Dependency injection self.
    """
    def __init__(self, config) -> None:
        self._config:dict = config

        self._fields_config = dict()
        "json configuration of fields"
    
        self._entity = dict()
        "instances of Entity"

        self._tools:dict = dict()
        "instances of Tools"

        self._field:dict = dict()
        "instances of Field"

        self._mapping:dict = dict()
        "instances of Mapping"
    
        self._condition:dict = dict()
        "instances of Condition"

        self._conn = mysql.connector.connect(
            host=self._config["host"],
            user=self._config["user"],
            password=self._config["password"],
            database=self._config["database"]
        )

        with open(self._config["path_model"]+"entity-tree.json", 'r', encoding='utf-8') as file:
            self._tree = json.load(file)

        with open(self._config["path_model"]+"entity-relations.json", 'r', encoding='utf-8') as file:
            self._relations = json.load(file)
    
        with open(self._config["path_model"]+"_entities.json", 'r', encoding='utf-8') as file:
            self._entities_config = json.load(file)

        if exists(self._config["path_model"]+"entities.json"):
            with open(self._config["path_model"]+"entities.json", 'r', encoding='utf-8') as file:
                e2 = json.load(file)

                for k, v in self._entities_config.items():
                    if k in e2:
                        self._entities_config[k].update(e2[k])

                for k, v in e2.items():
                    if k not in self._entities_config:
                        self._entities_config[k] = e2[k]

    def __del__(self):
        self._conn.close()

    def conn(self):
        return self._conn

    def tree_config(self) -> dict:
        return self._tree

    def relations_config(self) -> dict:
        return self._relations     

    def entities_config(self, entity_name):
        """ 
        configuracion de entidad

        Por cada entidad consultada es obligatorio que haya una configuracion
        """
        return self._entities_config[entity_name]

    def field_config(self, entity_name, field_name):
        """ 
        configuracion de field

        Si no existe el field consultado se devuelve una configuracion vacia
        No es obligatorio que exista el field en la configuracion, se cargaran los parametros por defecto.
        """
        config = self.fields_config(entity_name) 
        return config[field_name] if field_name in config else {} 

    def fields_config(self, entity_name) -> dict:
        """ 
        configuracion completa de fields de una entidad

        Por cada entidad consultada es obligatorio que haya una configuracion de fields
        """
        if entity_name not in self._fields_config:
            with open(self._config["path_model"]+"fields/_"+entity_name+".json", 'r', encoding='utf-8') as file:
                self._fields_config[entity_name] = json.load(file)

            if exists(self._config["path_model"]+"fields/"+entity_name+".json"):
                with open(self._config["path_model"]+"fields/"+entity_name+".json", 'r', encoding='utf-8') as file:
                    e2 = json.load(file)

                    for k, v in self._fields_config[entity_name].items():
                        if k in e2:
                            self._fields_config[entity_name][k].update(e2[k])

                    for k, v in e2.items():
                        if k not in self._fields_config[entity_name]:
                            self._fields_config[entity_name][k] = e2[k]

        return self._fields_config[entity_name] 
         
    def tree(self, entity_name: str) -> dict:
        return self._tree[entity_name]
    
    def relations(self, entity_name) -> dict:
        return self._relations[entity_name]       
    
    def entity_names(self) -> list:
        return list(self._tree.keys())

    def field_names(self, entity_name) -> list:
        return list(self.fields_config(entity_name).keys())
    
    def entity(self, entity_name:str) -> Entity:
        if entity_name not in self._entity:
            self._entity[entity_name] = Entity(self, entity_name)

        return self._entity[entity_name]

    def field(self, entity_name, field_name) -> Field:
        if entity_name not in self._field:
            self._field[entity_name] = dict()

        if field_name not in self._field[entity_name]:
            self._field[entity_name][field_name] = Field(self, entity_name, field_name)

        return self._field[entity_name][field_name]

    def query(self, entity_name) -> EntityQuery:
        return EntityQuery(self, entity_name)
    
    def tools(self, entity_name) -> EntityTools:
        if entity_name not in self._tools:
            self._tools[entity_name] = EntityTools(self, entity_name)

        return self._tools[entity_name]
    
    def explode_field(self, entity_name:str, field_name:str) -> dict:
        f = field_name.split('-') 

        if(len(f) == 2):
            return {
                "field_id": f[0],    
                "entity_name": self.relations(entity_name)[f[0]]["entity_name"],
                "field_name": f[1]
            }
        else:
            return {
                "field_id": "",
                "entity_name": entity_name,
                "field_name": field_name
            }
        
    def field_by_id(self, entity_name:str, field_id:str) -> Field:
        r = self.relations(entity_name)
        return self.field(entity_name, r[field_id]["field_name"])
    
    def mapping(self, entity_name: str, field_id:str = "") -> Mapping:
        if entity_name in self._mapping:
            return self._mapping[entity_name]

        try:
            m = importlib.import_module("src.mapping."+entity_name)
            Mapping_ = getattr(m, snake_case_to_camel_case(entity_name)+"Mapping")
            self._mapping[entity_name] = Mapping_(self, entity_name, field_id)

        except ModuleNotFoundError:
            self._mapping[entity_name] = Mapping(self, entity_name, field_id)
        
        return self._mapping[entity_name]
    
    def condition(self, entity_name: str, field_id:str = "") -> Condition:
        if entity_name in self._condition:
            return self._condition[entity_name]

        try:
            m = importlib.import_module("src.condition."+entity_name)
            Condition_ = getattr(m, snake_case_to_camel_case(entity_name)+"Condition")
            self._condition[entity_name] = Condition_(self, entity_name, field_id)

        except ModuleNotFoundError:
            self._condition[entity_name] = Condition(self, entity_name, field_id)
        
        return self._condition[entity_name]

    def values(self, entity_name: str, field_id:str = "") -> Condition:
        try:
            m = importlib.import_module("src.values."+entity_name)
            Values_ = getattr(m, snake_case_to_camel_case(entity_name)+"Values")
            return Values_(self, entity_name, field_id)

        except ModuleNotFoundError:
            return Values(self, entity_name, field_id)