import pytest
from pathlib import Path

from day04.commons.extract_util import ExtractUtil
from day04.commons.model_util import verify_yaml
from day04.commons.requests_util import RequestUtil
from day04.commons.yml_util import YmlUtil

eu=ExtractUtil()

class TestAllCase():
    pass


# 根据一个 yml 的路径创建一个测试用例的函数并且返回这个函数
def create_testcase(yaml_path):
    @pytest.mark.parametrize("caseinfo", YmlUtil().read_yml(yaml_path))
    def func(self, caseinfo):
        # 获取 yml 中发送请求四要素
        new_caseinfo = verify_yaml(caseinfo)
        # 从extract.yml中提取中间参数，加入到 requests 中
        # 请求中多添加一些参数也没有影响
        # 因此不管 extract.yml 中有没有数据都提取出来放到 requests 中也没啥影响
        new_request = eu.use_extract_value(new_caseinfo.request)
        # 发送请求
        res = RequestUtil().send_all_request(**new_request)
        # 发送请求后得到响应  如果有中间变量就 再提取中间变量（如token）
        if new_caseinfo.extract:
            for key, value in new_caseinfo.extract.items():
                eu.extract(res,key,*value)
        assert "success" in res.text or "本站新帖" in res.text
    return func


# 循环获取所有的 yml 文件（一个 yml 生成一个用例，然后把用例放到类下面）
testcases_path = Path(__file__).parent
print(testcases_path)
yml_case_list = testcases_path.glob('**/test_*.yml')
for yml_case in yml_case_list:
    create_testcase(yml_case)
    # 通过反射，这个循环每循环一个那么就生成一个函数，然后把这个函数加入到TestAllCase下面
    setattr(TestAllCase, "test_" + yml_case.stem, create_testcase(yml_case))
