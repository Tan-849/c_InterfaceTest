import copy

import pymysql


class AssertUtil():

    # 链接数据库
    def conn_database(self):
        self.conn = pymysql.connect(
            user="root",
            password="123456",
            host="localhost",
            port=3306,
            database="qi_api",
        )
        return self.conn

    # 执行SQL
    def execute_sql(self, sql):
        # 创建数据库连接
        conn = self.conn_database()
        # 创建游标
        cs = conn.cursor()
        # 执行SQL
        cs.execute(sql)
        # 取值
        value = cs.fetchone()
        # 关闭资源
        cs.close()
        conn.close()
        # 返回值
        return value

    # 断言封装
    def assert_all_case(self, res, assert_type, value):
        # 1.深拷贝一个 res
        new_res = copy.deepcopy(res)

        # 2.把 res.json() 改成 res.json
        try:
            new_res.json = new_res.json()
        except Exception:
            new_res.json = {"msg": "response not json data"}

        # 3.循环判断断言
        for msg, expect_and_actual_data in value.items():
            expect, actual = expect_and_actual_data[0], expect_and_actual_data[1]
            # 此时的 actual 只是 yml 文件的数据，需要根据这个数据从响应报文中获得实际的数据

            # 因此根据 yml 的数据获得响应对象中属性的值（利用反射）
            try:
                actual_value = getattr(new_res, actual)
            except Exception:
                print(f"警告：响应报文中不存在{actual}属性!(实际结果已经从响应报文中提取出来，然后保存到 extract.yml 中)")
                actual_value=actual
            # print(assert_type, msg, expect, actual_value)

            # 判断断言，msg用来在打印日志是知道哪里有问题
            match assert_type:
                case "equals":
                    assert expect == actual_value, msg
                case "contains":
                    assert expect in str(actual_value), msg
                case "db_equals":
                    expect_value = self.execute_sql(expect)
                    assert expect_value[0] == actual_value, msg
                case "db_contains":
                    expect_value=self.execute_sql(expect)
                    assert expect_value[0] in actual_value, msg


