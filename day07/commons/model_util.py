from dataclasses import dataclass


@dataclass
class CaseInfo:
    # 必填
    feature: str
    story: str
    title: str
    request: dict
    validate: dict
    # 选填
    extract: dict = None
    parametrize: list = None


# 校验测试用例
def verify_yaml(caseinfo: dict):
    try:
        # 通过构造器（__init__方法）实现参数校验
        # 如果参数不合法会构造失败，然后报错
        new_caseinfo = CaseInfo(**caseinfo)
        return new_caseinfo
    except Exception:
        raise Exception("YAML测试用例不符合框架的规范！")
