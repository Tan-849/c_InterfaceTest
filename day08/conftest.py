import pytest
from day08.commons.yml_util import YmlUtil
from day08.config import setting


@pytest.fixture(scope="session",autouse=True)
def clean_extract():
    YmlUtil().clean_yml(setting.extract_yml)