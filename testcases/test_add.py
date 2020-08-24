"""
============================
Author:柠檬班-木森
Time:2020/2/28   21:21
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import os
import unittest
import jsonpath
from common.readexcel import ReadExcel
from common.handlepath import DATADIR
from library.ddt import ddt, data
from common.handleconfig import conf
from common.handlerequests import SendRequest
from common.handle_data import CaseDate, replace_data
from common.handlelog import log

file_path = os.path.join(DATADIR, "apicases.xlsx")


@ddt
class TESTAdd(unittest.TestCase):
    excel = ReadExcel(file_path, "add")
    cases = excel.read_data()
    request = SendRequest()

    @classmethod
    def setUpClass(cls):
        """管理员账户登录"""
        url = conf.get("env", "url") + "/member/login"
        data = {
            "mobile_phone": conf.get("test_data", "admin_phone"),
            "pwd": conf.get("test_data", "admin_pwd")
        }
        headers = eval(conf.get("env", "headers"))
        response = cls.request.send(url=url, method="post", json=data, headers=headers)
        res = response.json()
        token = jsonpath.jsonpath(res, "$..token")[0]
        token_type = jsonpath.jsonpath(res, "$..token_type")[0]
        member_id = str(jsonpath.jsonpath(res, "$..id")[0])
        # 将提取的数据保存到CaseData的属性中
        CaseDate.admin_token_value = token_type + " " + token
        CaseDate.admin_member_id = member_id

    @data(*cases)
    def test_add(self, case):
        # 第一步:准备数据
        url = conf.get("env", "url") + case["url"]
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(CaseDate, "admin_token_value")
        data = eval(replace_data(case["data"]))
        expected = eval(case["expected"])
        method = case["method"]
        row = case["case_id"] + 1
        # 第二步：发请求获取实际结果
        response = self.request.send(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 第三步：断言（比对预期结果和实际结果）
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 数据库校验

        except AssertionError as e:
            print("预期结果：", expected)
            print("实际结果：", res)
            self.excel.write_data(row=row, column=8, value="未通过")
            log.error("用例：{}，执行未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            log.info("用例：{}，执行未通过".format(case["title"]))
