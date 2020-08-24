"""
============================
Author:柠檬班-木森
Time:2020/2/26   20:15
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import os
import unittest
import jsonpath
from decimal import Decimal
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handlepath import DATADIR
from common.handleconfig import conf
from common.handlerequests import SendRequest
from common.handlelog import log
from common.connectdb import DB

file_path = os.path.join(DATADIR, "apicases.xlsx")


# @ddt
# class TestWithdraw(unittest.TestCase):
#     excel = ReadExcel(file_path, "withdraw")
#     cases = excel.read_data()
#     request = SendRequest()
#     db = DB()
#
#     @data(*cases)
#     def test_withdraw(self, case):
#         # 第一步：准备用例数据
#         url = conf.get("env", "url") + case["url"]
#         case["data"] = case["data"].replace("#phone#", conf.get("test_data", "phone"))
#         case["data"] = case["data"].replace("#pwd#", conf.get("test_data", "pwd"))
#         headers = eval(conf.get("env", "headers"))
#         # 判断是否是取现接口，取现接口则加上请求头
#         if case["interface"].lower() == "withdraw":
#             headers["Authorization"] = self.token_value
#             case["data"] = case["data"].replace("#member_id#", str(self.member_id))
#         data = eval(case["data"])
#         expected = eval(case["expected"])
#         method = case["method"]
#         row = case["case_id"] + 1
#         # 判断是否需要进行sql校验
#         if case["check_sql"]:
#             sql = case["check_sql"].format(conf.get("test_data","phone"))
#             start_money = self.db.find_one(sql)["leave_amount"]
#         # 第二步：调用接口，获取实际结果
#         response = self.request.send(url=url, method=method, json=data, headers=headers)
#         res = response.json()
#         # 判断是否是登录接口
#         if case["interface"].lower() == "login":
#             # 提取用户id保存为类属性
#             TestWithdraw.member_id = jsonpath.jsonpath(res, "$..id")[0]
#             token = jsonpath.jsonpath(res, "$..token")[0]
#             token_type = jsonpath.jsonpath(res, "$..token_type")[0]
#             # 提取token,保存为类属性
#             TestWithdraw.token_value = token_type + " " + token
#         # 第三步：断言（比对预期结果和实际结果）
#         try:
#             self.assertEqual(expected["code"], res["code"])
#             self.assertEqual(expected["msg"], res["msg"])
#             if case["check_sql"]:
#                 sql = case["check_sql"].format(conf.get("test_data","phone"))
#                 end_money = self.db.find_one(sql)["leave_amount"]
#                 # 比对取现金额是否正确
#                 self.assertEqual(Decimal(str(data["amount"])),start_money-end_money)
#         except AssertionError as e:
#             print("预期结果：", expected)
#             print("实际结果：", res)
#             self.excel.write_data(row=row, column=8, value="未通过")
#             log.error("用例：{}，执行未通过".format(case["title"]))
#             log.exception(e)
#             raise e
#         else:
#             self.excel.write_data(row=row, column=8, value="通过")
#             log.info("用例：{}，执行未通过".format(case["title"]))
#


@ddt
class TestWithdraw(unittest.TestCase):
    excel = ReadExcel(file_path, "withdraw")
    cases = excel.read_data()
    request = SendRequest()
    db = DB()

    @data(*cases)
    def test_withdraw(self, case):
        # 第一步：准备用例数据
        url = conf.get("env", "url") + case["url"]
        case["data"] = case["data"].replace("#phone#", conf.get("test_data", "phone"))
        case["data"] = case["data"].replace("#pwd#", conf.get("test_data", "pwd"))
        headers = eval(conf.get("env", "headers"))
        # 判断是否是取现接口，取现接口则加上请求头
        if case["interface"].lower() == "withdraw":
            headers["Authorization"] = self.token_value
            case["data"] = case["data"].replace("#member_id#", str(self.member_id))
        data = eval(case["data"])
        expected = eval(case["expected"])
        method = case["method"]
        row = case["case_id"] + 1
        # 判断是否需要进行sql校验
        if case["check_sql"]:
            sql = case["check_sql"].format(conf.get("test_data","phone"))
            start_money = self.db.find_one(sql)["leave_amount"]
        # 第二步：调用接口，获取实际结果
        response = self.request.send(url=url, method=method, json=data, headers=headers)
        res = response.json()
        # 判断是否是登录接口
        if case["interface"].lower() == "login":
            # 提取用户id保存为类属性
            TestWithdraw.member_id = jsonpath.jsonpath(res, "$..id")[0]
            token = jsonpath.jsonpath(res, "$..token")[0]
            token_type = jsonpath.jsonpath(res, "$..token_type")[0]
            # 提取token,保存为类属性
            TestWithdraw.token_value = token_type + " " + token
        # 第三步：断言（比对预期结果和实际结果）
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            if case["check_sql"]:
                sql = case["check_sql"].format(conf.get("test_data","phone"))
                end_money = self.db.find_one(sql)["leave_amount"]
                # 比对取现金额是否正确
                self.assertEqual(Decimal(str(data["amount"])),start_money-end_money)
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
