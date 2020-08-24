import unittest
import os
from common.handlepath import CASEDIR,REPORTDIR
from library.HTMLTestRunnerNew import HTMLTestRunner
from common.handle_email import send_email
# 第一步：创建套件
suite = unittest.TestSuite()

# 第二步：加载用例到套件
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASEDIR))
# from testcases import test_main_stream
# suite = unittest.defaultTestLoader.loadTestsFromModule(test_main_stream)
report_file = os.path.join(REPORTDIR,"report1.html")
# 第三步：执行用例
runner = HTMLTestRunner(stream=open(report_file, "wb"),
                        description="第一次接口测试报告",
                        title="py26测试报告",
                        tester="musen"
                        )

runner.run(suite)
send_email(report_file,"py26测试报告最终版")
