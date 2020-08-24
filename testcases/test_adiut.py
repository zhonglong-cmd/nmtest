"""
============================
Author:柠檬班-木森
Time:2020/3/2   20:07
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import unittest
import os
import jsonpath
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handlepath import DATADIR
from common.handleconfig import conf
from common.handlerequests import SendRequest
from common.handlelog import log
from common.handle_data import replace_data, CaseDate
from common.connectdb import DB

file_path = os.path.join(DATADIR, "apicases.xlsx")

"""
关于审核的步骤分析：
1、要登录（所有的审核用例执行之前，登录就可以的）
2、加标（每一个用例执行之前都要加标）
3、审核




"""


@ddt
class TestAudit(unittest.TestCase):
    excel = ReadExcel(file_path, "audit")
    cases = excel.read_data()
    request = SendRequest()
    db = DB()

    @classmethod
    def setUpClass(cls) -> None:
        """进行登录"""
        # 1、准备登录的数据
        url = conf.get("env", "url") + "/member/login"
        data = {
            "mobile_phone": conf.get("test_data", "admin_phone"),
            "pwd": conf.get("test_data", "admin_pwd")
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
        CaseDate.admin_token_value = token_type + " " + token
        # 提取用户的id，设为CaseData类属性
        CaseDate.admin_member_id = str(jsonpath.jsonpath(res, "$..id")[0])

    def setUp(self) -> None:
        """进行加标"""
        # 1、准备加标的数据
        url = conf.get("env", "url") + "/loan/add"
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(CaseDate, "admin_token_value")
        data = {"member_id": getattr(CaseDate, "admin_member_id"),
                "title": "借钱实现财富自由",
                "amount": 2000,
                "loan_rate": 12.0,
                "loan_term": 3,
                "loan_date_type": 1,
                "bidding_days": 5}
        # 2、发送请求，添加项目
        response = self.request.send(url=url, method="post", json=data, headers=headers)
        res = response.json()
        # 3、提取审核需要用到的项目id
        CaseDate.loan_id = str(jsonpath.jsonpath(res, "$..id")[0])

    @data(*cases)
    def test_audit(self, case):
        # 第一步：准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(CaseDate, "admin_token_value")
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        # 第二步：发送请求，获取结果
        response = self.request.send(url=url, method=method, json=data, headers=headers)
        res = response.json()
        # 判断是否是审核通过的这条用例，并且审核通过
        if res["code"] == 0 and case["title"] == "审核通过":
            CaseDate.pass_loan_id = str(data["loan_id"])

        # 第三步：断言（比对预期结果和实际结果）
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 判断是否需要进行sql校验
            if case["check_sql"]:
                sql = replace_data(case["check_sql"])
                status = self.db.find_one(sql)["status"]
                # 断言数据库中的标状态字段是否和预期一致。
                self.assertEqual(expected["status"], status)
        except AssertionError as e:
            print("预期结果", expected)
            print("实际结果", res)
            self.excel.write_data(row=row, column=8, value="未通过")
            log.error("用例：{}，执行未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            log.info("用例：{}，执行未通过".format(case["title"]))
