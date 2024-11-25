import re

import pytest

from day03.commons.requests_util import RequestUtil
from day03.commons.yml_util import YmlUtil


class TestApi():
    temp_path="./testcases/phpwind/temp.yml"
    test_phpwind_yml_path="./testcases/phpwind/test_phpwind.yml"
    test_login_yml_path = "./testcases/phpwind/test_login.yml"

    @pytest.mark.parametrize("case_info",YmlUtil().read_yml(yaml_path=test_phpwind_yml_path))
    def test_phpwind(self,case_info):
        res = RequestUtil().send_all_request(method=case_info["request"]["method"], url=case_info["request"]["url"])
        search_value = re.search('name="csrf_token" value="(.*?)"', res.text)
        YmlUtil().white_yml(TestApi.temp_path,{"token": search_value.group(1)})
        assert "本站新帖" in res.text

    @pytest.mark.parametrize("case_info", YmlUtil().read_yml(yaml_path=test_login_yml_path))
    def test_login(self,case_info):
        urls = case_info["request"]["url"]
        datas = case_info["data"]
        datas["csrf_token"] = YmlUtil().read_yml(TestApi.temp_path,"token")
        headers = case_info["headers"]
        res = RequestUtil().send_all_request(method="post", url=urls, data=datas, headers=headers)
        print(res.json())

