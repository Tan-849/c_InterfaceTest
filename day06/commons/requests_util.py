import copy
import logging

import requests

# 生成日志对象
logger =  logging.getLogger(__name__)

# 统一请求封装
class RequestUtil:
    # 多个请求必须是同一个 session
    sess = requests.session()

    def send_all_request(self, **kwargs):
        # 处理公共参数
        total_params = {
            "application": "app",
            "application_client_type": "h5"
        }
        for key, value in kwargs.items():
            if key == "params":
                kwargs["params"].update(total_params)
            elif key == "files":
                for file_key, file_value in value.items():
                    value[file_key] = open(file_value, "rb")
        res = RequestUtil.sess.request(**kwargs)
        logger.info(res.text)
        return res
