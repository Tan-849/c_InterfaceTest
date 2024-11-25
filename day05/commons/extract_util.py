import copy
import re
from string import Template

import jsonpath
import yaml

from day05.commons.yml_util import YmlUtil
from day05.hotload.DebugTalk import DebugTalk


class ExtractUtil:
    extract_path = "./testcases/phpwind/temp.yml"

    # 解析提取变量保存到 extract_path
    def extract(self, res, var_name, attr_name, expr, index):
        """
        :param res: 发送请求后得到的响应数据
        :param var_name: 中间参数的名字（token/....） 用于 其他用例发送请求时调用
        :param attr_name: 提取中间参数的地方 （res.text / res.json() / res.cookie....）
        :param expr: 提取变量的方式（re正则表达式 / jsonpath）
        :param index: 变量的下标（通常为 1）
        :return:
        """

        # 深拷贝 避免对原来的结果产生影响
        new_res = copy.deepcopy(res)
        # json() 方法转为属性
        try:
            new_res.json = new_res.json()
        except Exception:
            new_res.json = {"msg": 'response not json data'}

        # 通过反射获取属性的值
        data = getattr(new_res, attr_name)
        # 判断用什么方式搜索出所需要的中间参数
        if expr.startswith("$"):
            list_temp = list(jsonpath.jsonpath(data, expr))
        else:
            list_temp = list(re.findall(expr, data))
        # 取出中间参数写入 exract.yml
        if list_temp:
            YmlUtil().white_yml(self.extract_path, {var_name: list_temp[index]})

    # 解析使用变量，把 $[access_.token] 替换从extract.yml 里面提取的具体的值
    def expr_replace_template(self, request_data: dict):
        # 1. 字典转换为字符串
        data_str = yaml.safe_dump(request_data)
        # 2. 字符串替换
        new_request_data = Template(data_str).safe_substitute(YmlUtil().read_yml(self.extract_path))
        # 3. 字符串还原成字典
        data_dict = yaml.safe_load(new_request_data)
        return data_dict

    def expr_replace_hotload(self, request_data: dict):
        # 字典转换为字符串
        data_str = yaml.safe_dump(request_data)

        # 定义一个正则匹配这种表达式
        # regexp = "\\$\\{(.*?)\}"                # ${number}
        regexp = "\\$\\{(.*?)\\((.*?)\\)\\}"  # ${函数名(参数)}
        # 通过正则表达式在data str字符串中去匹配，得到所有的表达式1ist
        fun_list = re.findall(regexp, data_str)
        for f in fun_list:
            # 从 yml 文件读取到了要调用哪个函数后，利用反射执行函数
            if f[1] == "":  # f[1] 为空代表调用无参方法
                new_value = getattr(DebugTalk(), f[0])()
            else:  # 有参方法
                new_value = getattr(DebugTalk(), f[0])(*f[1].split(","))

            # 如果 new_value 是一个字符串类型的数字 value应该加单引号
            if isinstance(new_value, str) and new_value.isdigit():
                new_value = "'" + new_value + "'"
            # 拼接旧的值
            old_value="${"+f[0]+"("+f[1]+")}"
            data_str=data_str.replace(old_value, str(new_value))
        # 3. 字符串还原成字典
        data_dict = yaml.safe_load(data_str)
        return data_dict
