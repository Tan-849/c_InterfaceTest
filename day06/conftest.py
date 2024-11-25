import pytest
from day06.commons.yml_util import YmlUtil
@pytest.fixture(scope="session",autouse=True)
def clean_extract():
    YmlUtil().clean_yml("./testcases/phpwind/temp.yml")