"""
============================
Author:柠檬班-木森
Time:2020/2/12   19:33
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""

"""
配置文件类的封装

封装的目的：使用更简单


封装的需求：
    1、简化创建配置文件解析器对象，加载配置文件的流程（需要封装），提示（重写init方法）
    2、读取数据（不进行封装，使用原来的方法），通过继承父类即可
    3、简化写入数据的操作（需要封装），提示：自定义一个write_data方法。

"""
import os
from configparser import ConfigParser
from common.handlepath import CONFDIR


class HandleConfig(ConfigParser):

    def __init__(self, filename):
        # 调用父类的init方法
        super().__init__()
        self.filename = filename
        self.read(filename,encoding="utf8")

    def write_data(self, section, options, value):
        """写入数据的方法"""
        self.set(section, options, value)
        self.write(fp=open(self.filename, "w"))


conf = HandleConfig(os.path.join(CONFDIR,"config.ini"))