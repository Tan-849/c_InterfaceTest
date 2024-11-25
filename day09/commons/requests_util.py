import copy
import logging
import traceback

import requests

from day09.config import setting

# 生成日志对象
logger =  logging.getLogger(__name__)

# 统一请求封装
class RequestUtil:
    # 多个请求必须是同一个 session
    sess = requests.session()

    def send_all_request(self, **kwargs):
        # 处理公共参数
        total_params = setting.global_args
        for key, value in kwargs.items():
            if key == "params":
                kwargs["params"].update(total_params)
            try:
                if key == "files":
                    for file_key, file_value in value.items():
                        value[file_key] = open(file_value, "rb")
            except Exception :
                logger.error("文件路径有误！")
            # 请求四要素写到日志里
            logger.info(f"请求报文：{key} = {value}")

        try:
            res = RequestUtil.sess.request(**kwargs)
        except Exception as e:
            logger.error(f"请求出现异常！没有接收到响应！{str(traceback.format_exc())}")
            raise e

        # 判断返回的内容是否是一个json格式
        if "json" in res.headers.get("Content-Type"):
            logger.info(f"响应数据：{res.json()}")
        else:
            logger.info("响应报文太长不显示再日志内！")
        return res
