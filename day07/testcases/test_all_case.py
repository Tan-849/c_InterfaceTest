import allure
import pytest
from pathlib import Path

from day07.commons.ddt_util import read_testcase
from day07.commons.main_util import stand_case_flow
from day07.commons.model_util import verify_yaml


class TestAllCase():
    pass


# 根据一个 yml 的路径创建一个测试用例的函数并且返回这个函数
def create_testcase(yaml_path):
    @pytest.mark.parametrize("caseinfo", read_testcase(yaml_path))
    def func(self, caseinfo):
        global case_obj
        if isinstance(caseinfo, list): # 多接口用例
            for case in caseinfo:
                # 1.获取 yml 中发送请求四要素并校验
                case_obj = verify_yaml(case)
                # 用例标准化执行流程
                stand_case_flow(case_obj)
        else: # 单接口用例
            # 1.获取 yml 中发送请求四要素并校验
            case_obj = verify_yaml(caseinfo)
            # 用例标准化执行流程
            stand_case_flow(case_obj)
        # 定制 Allure 报告
        allure.dynamic.feature(case_obj.feature)
        allure.dynamic.story(case_obj.story)
        allure.dynamic.title(case_obj.title)
    return func


# 循环获取所有的 yml 文件（一个 yml 生成一个用例，然后把用例放到类下面）
testcases_path = Path(__file__).parent # 获取当前文件的路径
print(testcases_path)
yml_case_list = testcases_path.glob('**/test_*.yml')
for yml_case in yml_case_list:
    create_testcase(yml_case)
    # 通过反射，这个循环每循环一个那么就生成一个函数，然后把这个函数加入到TestAllCase下面
    setattr(TestAllCase, "test_" + yml_case.stem, create_testcase(yml_case))


