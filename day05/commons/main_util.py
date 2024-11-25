from day05.commons.extract_util import ExtractUtil
from day05.commons.model_util import verify_yaml
from day05.commons.requests_util import RequestUtil

eu = ExtractUtil()
re = RequestUtil()


def stand_case_flow(caseinfo):
    # 获取 yml 中发送请求四要素
    case_obj = verify_yaml(caseinfo)

    # 发送请求前，从 extract.yml 中提取中间参数（比如token），
    # 添加到 requests 中（无论 extract.yml 有没有数据，因为不会影响发送请求）
    # 发送请求后得到响应 res
    # res = re.send_all_request(**eu.expr_replace_template(case_obj.request))
    res = re.send_all_request(**eu.expr_replace_hotload(case_obj.request))
    pass

    # 断言
    assert "success" in res.text or "本站新帖" in res.text

    # 如果 yml 文件中指明要提取（${xxxxx}）中间变量就执行
    if case_obj.extract:
        for key, value in case_obj.extract.items():
            # res 为需要提取中间变量的所有响应数据
            # key 为提取的中间变量的key(通常将这个中间变量命名为token)
            # *value 解包后就有 attr_name(提取地方=res.attr_name), expr(提取方式=正则表达式), index(下标)
            eu.extract(res, key, *value)


