import re

from day02.commons.requests_util import RequestUtil


class Testapi1():

    def test_login(self):
        print("登录")

        # params={
        #     "name1": "tanhaowei",
        #     "name2": "Thw"
        # }
        # requests.get(url="http://47.107.116.139/phpwind/", params=params)

        # datas = {
        #     "name1": "tanhaowei",
        #     "name2": "Thw"
        # }
        # requests.get(url="http://47.107.116.139/phpwind/", data=datas)

        # jsons = {
        #     "name1": "tanhaowei",
        #     "name2": "谭豪伟"
        # }
        # requests.get(url="http://47.107.116.139/phpwind/", json=jsons)

        # files = {
        #     "uploads": open("./tanhaowei.png", "rb")
        # }
        # requests.get(url="http://47.107.116.139/phpwind/", files=files)

        # res = requests.get(url="http://47.107.116.139/phpwind/")
        # res.text
        # res.content  # 返回二进制类型的数据
        # res.json()  # 把json字符串转化为字典格式返回 ====== 这是一个方法
        # res.status  # code状态码
        # res.reason  # 状态信息
        # res.cookies  # cookie信息
        # res.encoding  # 编码格式
        # res.headers  # 响应头
        # res.elapsed  # 耗时
        # res.request.method  # 请求方式
        # res.request.url  # 请求路径
        # res.request.headers  # 请求头
        # res.request.body  # 请求数据

        # res = requests.get(url="http://47.107.116.139/phpwind/")
        # print(res.text)

        # # 第 1 种
        # requests.get(url="xxx", params="xxx")
        # requests.post(url="xxx", data="xxx", json="xxx")
        # requests.put(url="xxx", data="xxx")
        # requests.delete(url="xxx")
        # # 第 2 种
        # requests.request(method="xxx", url="xxx")
        # # 第 3 种
        # requests.session().request(self,
        #                            method="post",
        #                            url="xxx",
        #                            params=None,
        #                            data=None,
        #                            headers=None,
        #                            cookies=None,
        #                            files=None,
        #                            auth=None,
        #                            timeout=None,
        #                            allow_redirects=True,
        #                            proxies=None,
        #                            hooks=None,
        #                            stream=None,
        #                            verify=None,
        #                            cert=None,
        #                            json=None,
        #                            )

    token = ""
    access_token=""

    def test_phpwind(self):
        urls = "http://47.107.116.139/phpwind/"
        res = RequestUtil().send_all_request(method="post", url=urls)
        assert "本站新帖" in res.text
        search_value = re.search('name="csrf_token" value="(.*?)"', res.text)
        Testapi1.token = search_value.group(1)

    def test_login1(self):
        urls = "http://47.107.116.139/phpwind/index.php?m=u&c=login&a=dorun"
        datas = {
            "username": "tanhaowei",
            "password": "123456",
            "csrf_token": Testapi1.token,
            "backurl": "http://47.107.116.139/phpwind/",
            "invite": ""
        }
        headerss = {
            "Accept": "application/json,text/javascript,/q=0.01",
            "X-Requested-With": "XMLHttpRequest"
        }
        res = RequestUtil().send_all_request(method="post", url=urls, data=datas, headers=headerss)
        print(res.json())

    def test_file_upload(self):
        url = "https://api.weixin.qq.com/cgi-bin/media/uploadimg"
        params = {
            "access token": Testapi1.access_token,
            }
        data = {
            "media": "./tanhaowei.png"
            }
        res =RequestUtil().send_all_request(method="post", url=url, params=params, files=data)
        print(res.json())
