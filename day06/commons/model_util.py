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


# 校验测试用例
def verify_yaml(caseinfo: dict):
    try:
        # 通过构造器（__init__方法）实现参数校验
        # 如果参数不合法会构造失败，然后报错
        new_caseinfo = CaseInfo(**caseinfo)
        return new_caseinfo
    except Exception:
        raise Exception("YAML测试用例不符合框架的规范！")

# 测试参数校验方法是否有效
# if __name__ == '__main__':
#     a = {
#         'feature': '论坛模块',
#         'story': 'phpwind首页接口',
#         'title': '验证phpwind首页接口正常返回',
#         'request': {
#             'method': 'post',
#             'url': 'http:/101.34.221.219:8010/api.php',
#             'params': {
#                 's': 'index/index'
#             }
#         },
#         'validate': None
#     }
#     new_caseinfo = verify_yaml(a)
#     print(new_caseinfo.feature)
#     print(new_caseinfo.title)
#     print(new_caseinfo.request)
#     print(new_caseinfo)
