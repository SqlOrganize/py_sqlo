import importlib
import mysql.connector
from mysql.connector.connection import MySQLConnection
import json
from os.path import exists

from py_sqlo.src.entity_options.entity_options import EntityOptions
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
        self.config:dict = {
            "host":"",
            "user":"",
            "password":"",
            "database":"",
            "path_json":""
        }

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
        "instances of Mapping"

        self._con = mysql.connector.connect(
            host=self.config["host"],
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"]
        )

        with open(self.config["path_model"]+"entity-tree.json", 'r', encoding='utf-8') as file:
            self._tree = json.load(file)

        with open(self.config["path_model"]+"entity-relations.json", 'r', encoding='utf-8') as file:
            self._relations = json.load(file)
    
        with open(self.config["path_model"]+"_entities.json", 'r', encoding='utf-8') as file:
            self._entities_config = json.load(file)

        if exists(self.config["path_model"]+"entities.json"):
            with open(self.config["path_model"]+"entities.json", 'r', encoding='utf-8') as file:
                e2 = json.load(file)

                for k, v in self._entities_config.items():
                    if k in e2:
                        self._entities_config[k].update(e2[k])

                for k, v in e2.items():
                    if k not in self._entities_config:
                        self._entities_config[k] = e2[k]

    def __del__(self):
        self._con.close()

    def tree_config(self) -> dict:
        return self._tree

    classmethod
    def relations_config(self) -> dict:
        return self._relations     

    
    def entities_config(self, entity_name):
        return self._entities_config[entity_name]

    def fields_config(self, entity_name) -> dict:
        if entity_name not in self._fields_config:
            with open(self.config["path_model"]+"fields/_"+entity_name+".json", 'r', encoding='utf-8') as file:
                self._fields_config[entity_name] = json.load(file)

            if exists(self.config["path_model"]+"fields/"+entity_name+".json"):
                with open(self.config["path_model"]+"fields/"+entity_name+".json", 'r', encoding='utf-8') as file:
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
            self._entity[entity_name] = Entity(self, self._entities_config[entity_name])

        return self._entity[entity_name]

    
    def field(self, entity_name, field_name) -> Field:
        if entity_name not in self._field:
            self._field[entity_name] = dict()

        if field_name not in self._field[entity_name]:
            if field_name in self.fields_config(entity_name):
                cfg = self.fields_config(entity_name)[field_name]
                self._field[entity_name][field_name] = Field(self, cfg)
            else:
                self._field[entity_name][field_name] = Field(self, {
                    "entity_name":entity_name,
                    "name":field_name
                })

        return self._field[entity_name][field_name]

    
    def query(self, entity_name) -> EntityQuery:
        return EntityQuery(entity_name)

    
    def tools(self, entity_name) -> EntityTools:
        if entity_name not in self._tools:
            self._tools[entity_name] = EntityTools(entity_name)

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
            self._mapping[entity_name] = Mapping_(entity_name, field_id)

        except ModuleNotFoundError:
            self._mapping[entity_name] = Mapping(entity_name, field_id)
        
        return self._mapping[entity_name]

    
    def condition(self, entity_name: str, field_id:str = "") -> Condition:
        if entity_name in self._condition:
            return self._condition[entity_name]

        try:
            m = importlib.import_module("src.condition."+entity_name)
            Condition_ = getattr(m, snake_case_to_camel_case(entity_name)+"Condition")
            self._condition[entity_name] = Condition_(entity_name, field_id)

        except ModuleNotFoundError:
            self._condition[entity_name] = Condition(entity_name, field_id)
        
        return self._condition[entity_name]
