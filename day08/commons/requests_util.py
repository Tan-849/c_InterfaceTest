import copy
import logging

import requests

from day08.config import setting

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
            elif key == "files":
                for file_key, file_value in value.items():
                    value[file_key] = open(file_value, "rb")
        res = RequestUtil.sess.request(**kwargs)
        # 判断返回的内容是否是一个json格式
        if "json" in res.headers.get("Content-Type"):
            logger.info(res.json())
        else:
            logger.info(res.text)
        return res
