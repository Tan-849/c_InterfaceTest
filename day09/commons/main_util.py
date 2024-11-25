import traceback

from day09.commons.assert_util import AssertUtil
from day09.commons.extract_util import ExtractUtil
from day09.commons.model_util import verify_yaml, CaseInfo
from day09.commons.requests_util import RequestUtil, logger

eu = ExtractUtil()
re = RequestUtil()
au = AssertUtil()

def stand_case_flow(case_obj:CaseInfo):
    logger.info(f"模块_接口_用例：{case_obj.feature}_{case_obj.story}_{case_obj.title}")
    # 2.发送请求
    # 发送请求前，从 extract.yml 中提取中间参数（比如token），
    # 添加到 requests 中（无论 extract.yml 有没有数据，因为不会影响发送请求）
    # 发送请求后得到响应 res
    # res = re.send_all_request(**eu.expr_replace_template(case_obj.request)) # template 有缺陷
    res = re.send_all_request(**eu.expr_replace_hotload(case_obj.request))

    # 3. 如果 yml 文件中指明要提取（${xxxxx}）中间变量就执行以下代码（从 res 中提取出中间变量）
    if case_obj.extract:
        for key, value in case_obj.extract.items():
            # res 为需要提取中间变量的所有响应数据
            # key 为提取的中间变量的key(通常将这个中间变量命名为token)
            # *value 解包后就有 attr_name(提取地方=res.attr_name), expr(提取方式=正则表达式), index(下标)
            eu.extract(res, key, *value)

    # 4.断言

    # 封装前断言，仍然需要修改 Python 代码才能实现断言，因此不完美
    # assert "success" in res.text or "本站新帖" in res.text

    # 封装代言（用 yml 文件而不是代码 实现断言）
    # 请求之后得到响应后，如果 validate 不为 None，则需要断言
    try:
        if case_obj.validate:
            for assert_type, value in eu.expr_replace_hotload(case_obj.validate).items():
                au.assert_all_case(res,assert_type, value)
            logger.info("断言成功！\n")
        else:
            logger.info("此用例没有配置断言！！！\n")
            print("此用例没有配置断言！！")
    except Exception as e:
        logger.error(f"断言失败！:{str(traceback.format_exc())}\n")
        raise e