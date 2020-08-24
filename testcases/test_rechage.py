"""
============================
Author:柠檬班-木森
Time:2020/2/21   21:49
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""

import unittest
import jsonpath
import os
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handlepath import DATADIR
from common.handleconfig import conf
from common.handlerequests import SendRequest
from common.handlelog import log
from common.connectdb import DB
from decimal import Decimal
from common.handle_data import CaseDate,replace_data

case_file = os.path.join(DATADIR, "apicases.xlsx")


@ddt
class TestRecharge(unittest.TestCase):
    excel = ReadExcel(case_file, "recharge")
    cases = excel.read_data()
    request = SendRequest()
    db = DB()

    @classmethod
    def setUpClass(cls):
        # 1、准备登录的数据
        url = conf.get("env", "url") + "/member/login"
        data = {
            "mobile_phone": conf.get("test_data", "phone"),
            "pwd": conf.get("test_data", "pwd")
        }
        headers = eval(conf.get("env", "headers"))
        # 3、发送请求，进行登录
        response = cls.request.send(url=url, method="post", json=data, headers=headers)
        # 获取返回的数据
        res = response.json()
        # 3、提取token,保存为类属性
        token = jsonpath.jsonpath(res, "$..token")[0]
        token_type = jsonpath.jsonpath(res, "$..token_type")[0]
        # 将提取到的token设为CaseData类属性
        CaseDate.token_value = token_type + " " + token
        # 提取用户的id，设为CaseData类属性
        CaseDate.member_id = str(jsonpath.jsonpath(res, "$..id")[0])


    @data(*cases)
    def test_recharge(self, case):
        # 第一步：准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        # 替换参数中的用户id
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(CaseDate,"token_value")
        # 在请求头中加入setupclass中提取出来的token
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        # 第二步：发送请求，获取结果
        # 发送请求之前,获取用余额
        if case["check_sql"]:
            sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}".format(
                conf.get("test_data", "phone"))
            # 查询当前用户的余额
            start_money = self.db.find_one(sql)["leave_amount"]

        response = self.request.send(url=url, method=method, json=data, headers=headers)
        res = response.json()
        # 发送请求之后,获取用余额
        if case["check_sql"]:
            sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}".format(
                conf.get("test_data", "phone"))
            # 查询当前用户的余额
            end_money = self.db.find_one(sql)["leave_amount"]
        # 第三步：断言（比对预期结果和实际结果）
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 判断示范需要进行sql校验
            if case["check_sql"]:
                self.assertEqual(end_money - start_money, Decimal(str(data["amount"])))
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



# @ddt
# class TestRecharge(unittest.TestCase):
#     excel = ReadExcel(case_file, "recharge")
#     cases = excel.read_data()
#     request = SendRequest()
#     db = DB()
#
#     @classmethod
#     def setUpClass(cls):
#         # 1、准备登录的数据
#         url = conf.get("env", "url") + "/member/login"
#         data = {
#             "mobile_phone": conf.get("test_data", "phone"),
#             "pwd": conf.get("test_data", "pwd")
#         }
#         headers = eval(conf.get("env", "headers"))
#         # 3、发送请求，进行登录
#         response = cls.request.send(url=url, method="post", json=data, headers=headers)
#         # 获取返回的数据
#         res = response.json()
#         # 3、提取token,保存为类属性
#         token = jsonpath.jsonpath(res, "$..token")[0]
#         token_type = jsonpath.jsonpath(res, "$..token_type")[0]
#         # 将提取到的token设为类属性
#         cls.token_value = token_type + " " + token
#         # 提取用户的id，保存为类属性
#         cls.member_id = jsonpath.jsonpath(res, "$..id")[0]
#
#     @data(*cases)
#     def test_recharge(self, case):
#         # 第一步：准备用例数据
#         url = conf.get("env", "url") + case["url"]
#         method = case["method"]
#         # 替换参数中的用户id
#         case["data"] = case["data"].replace("#member_id#", str(self.member_id))
#         data = eval(case["data"])
#         headers = eval(conf.get("env", "headers"))
#         headers["Authorization"] = self.token_value
#         # 在请求头中加入setupclass中提取出来的token
#         expected = eval(case["expected"])
#         row = case["case_id"] + 1
#         # 第二步：发送请求，获取结果
#         # 发送请求之前,获取用余额
#         if case["check_sql"]:
#             sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}".format(
#                 conf.get("test_data", "phone"))
#             # 查询当前用户的余额
#             start_money = self.db.find_one(sql)["leave_amount"]
#
#         response = self.request.send(url=url, method=method, json=data, headers=headers)
#         res = response.json()
#         # 发送请求之后,获取用余额
#         if case["check_sql"]:
#             sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}".format(
#                 conf.get("test_data", "phone"))
#             # 查询当前用户的余额
#             end_money = self.db.find_one(sql)["leave_amount"]
#         # 第三步：断言（比对预期结果和实际结果）
#         try:
#             self.assertEqual(expected["code"], res["code"])
#             self.assertEqual(expected["msg"], res["msg"])
#             # 判断示范需要进行sql校验
#             if case["check_sql"]:
#                 self.assertEqual(end_money - start_money, Decimal(str(data["amount"])))
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
