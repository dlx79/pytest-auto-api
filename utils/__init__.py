
from utils.read_files_tools.yaml_control import GetYamlData
from common.setting import ensure_path_sep
from utils.other_tools.models import Config


_data = GetYamlData(ensure_path_sep("/common/config.yaml")).get_yaml_data()
print('_data=',_data)
'''
from pydantic import BaseModel
class Person(BaseModel):
    name: str
    age: int
# 创建一个 Person 对象
person_data = {"name": "Alice", "age": 30}
person = Person(**person_data)

# 打印对象的属性
print(person.name)  # 输出: Alice
'''
config = Config(**_data)
print('config=',config)

