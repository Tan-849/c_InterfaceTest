import pytest
from commons.yaml_util import clean_yaml
@pytest.fixture(scope="session",autouse=True)
def clean_extract():
    clean_yaml()