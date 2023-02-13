import sys
sys.path.insert(0, "../")

from src.config import *
from src.container import Container
from pprint import pprint

config = {
    "user":"root",
    "password":"",
    "host":"localhost",
    "database":"planfi10_20203",
    "path_model":"C:\\xampp\\htdocs\\fines2-estructura\\model\\"
}

Container.init(config)

e = Container.entity("sede")
pprint(vars(e))

query = Container.query("toma").cond([
    [
        ["cond1", EQUAL, "value1"],
        ["cond2", EQUAL, "value2"],
    ],
    ["cond3", APPROX, "value3"],
]).order({"cond1":"ASC", "cond2":"DESC"}).add_prefix("pre-")

pprint(vars(query))

# print(Container.tools("persona").fieldNames())
# pprint(vars(Container.query("persona")))
# pprint(vars(Container.field("persona","nombres")))
# json_formatted_str = json.dumps(Container.entities(), indent=2)

# print(json_formatted_str)

# try:
#     Container.db_connect()
# finally:
#     Container.db_close()
