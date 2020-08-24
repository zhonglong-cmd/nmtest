"""
============================
Author:柠檬班-木森
Time:2020/2/14   21:13
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import os

# # 获取当前文件的绝对路径
# res = os.path.abspath(__file__)
# print(res)
# # 获取指定文件路径的父级目录路径
# res2 = os.path.dirname(res)
# print(res2)
#
# res3 = os.path.dirname(res2)
# print(res3)

# 项目目录路径
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用例模块目录的路径
CASEDIR = os.path.join(BASEDIR, "testcases")

# 用例数据目录的路径
DATADIR = os.path.join(BASEDIR, "data")

# 测试报告目录的路径
REPORTDIR = os.path.join(BASEDIR, "reports")

# 配置文件目录的路径
CONFDIR = os.path.join(BASEDIR, "conf")

# 日志文件目录
LOGDIR = os.path.join(BASEDIR, "logs")

# print(BASEDIR)
# print(CASEDIR)
# print(DATADIR)
# print(REPORTDIR)
# print(CONFDIR)
# print(LOGDIR)
