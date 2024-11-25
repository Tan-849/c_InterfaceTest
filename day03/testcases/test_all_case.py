from pathlib import Path

import pytest

from day03.commons.model_util import verify_yaml
from day03.commons.requests_util import RequestUtil
from day03.commons.yml_util import YmlUtil


class TestAllCase():
    pass


# 根据一个 yml 的路径创建一个测试用例的函数并且返回这个函数
def create_testcase(yaml_path):
    @pytest.mark.parametrize("caseinfo", YmlUtil().read_yml(yaml_path))
    def func(self, caseinfo):
        # 获取 yml 数据
        new_caseinfo = verify_yaml(caseinfo)
        # 发送请求
        RequestUtil().send_all_request(**new_caseinfo.request)
    return func


# 循环获取所有的 yml 文件（一个 yml 生成一个用例，然后把用例放到类下面）
testcases_path = Path(__file__).parent
print(testcases_path)
yml_case_list = testcases_path.glob('**/test_*.yml')
for yml_case in yml_case_list:
    create_testcase(yml_case)
    # 通过反射，这个循环每循环一个那么就生成一个函数，然后把这个函数加入到TestA11Case下面
    setattr(TestAllCase, "test_" + yml_case.stem, create_testcase(yml_case))
