import sys
import json

sys.path.insert(0, "../src")

from container import Container
from pprint import pprint

config = {
    "user":"root",
    "password":"",
    "host":"localhost",
    "database":"planfi10_20203",
    "path_model":"C:\\xampp\\htdocs\\fines2-estructura\\model\\"
}

Container.init(config)
tools = Container.tools("toma")
pprint(tools.fieldNames())
# pprint(vars(tools))

# print(Container.tools("persona").fieldNames())
# pprint(vars(Container.query("persona")))
# pprint(vars(Container.field("persona","nombres")))
# json_formatted_str = json.dumps(Container.entities(), indent=2)

# print(json_formatted_str)

# try:
#     Container.db_connect()
# finally:
#     Container.db_close()
