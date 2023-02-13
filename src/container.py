import mysql.connector
from mysql.connector.connection import MySQLConnection
import json
from os.path import exists
from src.icontainer import IContainer

from src.model.entity import Entity
from src.model.entity_query import EntityQuery
from src.model.entity_tools import EntityTools
from src.model.field import Field

class Container(IContainer):
    """ Dependency injection cls.
    """
    
    config:dict = {
        "host":"",
        "user":"",
        "password":"",
        "database":"",
        "path_json":""
    }

    db: MySQLConnection
    db_connections:int = 0

    _tree:dict = dict()
    "json configuration tree"

    _relations:dict = dict()
    "json configuration of relations"
    
    _entitiesConfig:dict = dict()
    "json configuration of entities"
    
    _fieldsConfig:dict = dict()
    "json configuration of fields"
    
    _entity:dict = dict()
    "instances of Entity"

    _tools:dict = dict()
    "instances of Tools"

    _field:dict = dict()
    "instances of Field"

    @classmethod
    def _init_tree(cls):
        if not cls._tree:
            with open(cls.config["path_model"]+"entity-tree.json", 'r', encoding='utf-8') as file:
                cls._tree = json.load(file)

    @classmethod
    def _init_relations(cls):
        if not cls._relations:
            with open(cls.config["path_model"]+"entity-relations.json", 'r', encoding='utf-8') as file:
                cls._relations = json.load(file)

    @classmethod
    def _init_entities_config(cls):
        if not cls._entitiesConfig:
            with open(cls.config["path_model"]+"_entities.json", 'r', encoding='utf-8') as file:
                cls._entitiesConfig = json.load(file)

            if exists(cls.config["path_model"]+"entities.json"):
                with open(cls.config["path_model"]+"entities.json", 'r', encoding='utf-8') as file:
                    e2 = json.load(file)

                    for k, v in cls._entitiesConfig.items():
                        if k in e2:
                            cls._entitiesConfig[k].update(e2[k])

                    for k, v in e2.items():
                        if k not in cls._entitiesConfig:
                            cls._entitiesConfig[k] = e2[k]

    @classmethod
    def init(cls, config):
        cls.config = config
        cls._init_tree()
        cls._init_relations()
        cls._init_entities_config()
        Entity.container = cls
        EntityQuery.container = cls
        EntityTools.container = cls

    @classmethod
    def db_connect(cls) -> MySQLConnection:
        """ Return an instance of db connector
            Make sure there is only a unique connection to db
        """    
        if cls.db_connections == 0:
            cls.db = mysql.connector.connect(
                host=cls.config["hosts    "],
                user=cls.config["user"],
                password=cls.config["password"],
                database=cls.config["database"]
            )

        cls.db_connections += 1

        return cls.db

    @classmethod
    def db_close(cls):
        if cls.db_connections == 0:
            raise Exception("No connections available") 

        elif cls.db_connections == 1:
            cls.db.close()

        cls.db_connections -= 1

    @classmethod
    def tree_config(cls) -> dict:
        return cls._tree

    classmethod
    def relations_config(cls) -> dict:
        return cls._relations     

    @classmethod
    def entities_config(cls):
        return cls._entitiesConfig

    @classmethod
    def fields_config(cls, entityName) -> dict:
        if entityName not in cls._fieldsConfig:
            with open(cls.config["path_model"]+"fields/_"+entityName+".json", 'r', encoding='utf-8') as file:
                cls._fieldsConfig[entityName] = json.load(file)

            if exists(cls.config["path_model"]+"fields/"+entityName+".json"):
                with open(cls.config["path_model"]+"fields/"+entityName+".json", 'r', encoding='utf-8') as file:
                    e2 = json.load(file)

                    for k, v in cls._fieldsConfig[entityName].items():
                        if k in e2:
                            cls._fieldsConfig[entityName][k].update(e2[k])

                    for k, v in e2.items():
                        if k not in cls._fieldsConfig[entityName]:
                            cls._fieldsConfig[entityName][k] = e2[k]

        return cls._fieldsConfig[entityName] 
        
    @classmethod
    def tree(cls, entityName) -> dict:
        return cls._tree[entityName]

    @classmethod
    def relations(cls, entityName) -> dict:
        return cls._relations[entityName]       
    
    @classmethod
    def entity_names(cls) -> list:
        return list(cls.tree().keys())

    @classmethod
    def field_names(cls, entityName) -> list:
        return list(cls.fields_config(entityName).keys())
    
    @classmethod
    def entity(cls, entityName) -> Entity:
        if entityName not in cls._entity:
            cls._entity[entityName] = Entity(cls._entitiesConfig[entityName])

        return cls._entity[entityName]

    @classmethod
    def field(cls, entityName, fieldName) -> Field:
        if entityName not in cls._field:
            cls._field[entityName] = dict()

        if fieldName not in cls._field[entityName]:
            cfg = cls.fields_config(entityName)[fieldName]
            cls._field[entityName][fieldName] = Field(cfg)

        return cls._field[entityName][fieldName]

    @classmethod
    def query(cls, entityName) -> EntityQuery:
        return EntityQuery(entityName)

    @classmethod
    def tools(cls, entityName) -> EntityTools:
        if entityName not in cls._tools:
            cls._tools[entityName] = EntityTools(entityName)

        return cls._tools[entityName]