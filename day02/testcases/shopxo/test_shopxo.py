import jsonpath
import requests

from day02.commons.requests_util import RequestUtil


class Test_shopxo():
    token = ""

    def test_start_list(self):
        method = "post"
        url = "http://101.34.221.219:8010/api.php"
        params = {
            "application": "app",
            "application_client_type": "h5",
            "token": "token",
            "ajax": "ajax",
            "s": "index/index"
        }
        res = RequestUtil().send_all_request(method=method, url=url, params=params)
        print(res.json())

    # 商品详情接口
    def test_product_detail(self):
        method = "post"
        url = "http://101.34.221.219:8010/api.php"
        params = {
            "s": "goods/detail"
        }
        json = {
            "goods_id": "12"
        }
        res = RequestUtil().send_all_request(method=method, url=url, params=params, json=json)
        print(res.json())

    # 登陆接口
    def test_login_shopxo(self):
        method = "post"
        url = "http://101.34.221.219:8010/api.php"
        params = {
            "s": "user/login"
        }
        json = {
            "accounts": "baili",
            "pwd": "baili123",
            "verify": "rib5",
            "type": "username"
        }
        res = RequestUtil().send_all_request(method=method, url=url, params=params, json=json)
        # 提取token
        Test_shopxo.token = jsonpath.jsonpath(res.json(), "$data.token")[0]

    # 订单列表接口
    def test_order_list(self):
        method = "post"
        url = "http://101.34.221.219:8010/api.php"
        params = {
            "token": Test_shopxo.token,
            "s": "order/index"
        }
        json = {
            "page": 1,
            "keywords": "",
            "status": "-1",
            "is_more": 1
        }
        res = RequestUtil().send_all_request(method=method, url=url, params=params, json=json)
        print(res.json())

    # 订单详情接口
    def test_order_detail(self):
        method = "post"
        url = "http://101.34.221.219:8010/api.php"
        params = {
            "token": Test_shopxo.token,
            "s": "order/detail"
        }
        json = {
            "id": "2597"
        }
        res = RequestUtil().send_all_request(method=method, url=url, params=params, json=json)
        print(res.json())
