"""
============================
Author:柠檬班-木森
Time:2020/2/21   20:34
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import requests


class SendRequest(object):
    """cookie+session鉴权的请求类封装"""

    def __init__(self):
        self.session = requests.session()

    def send(self, url, method, headers=None, params=None, data=None, json=None, files=None):
        method = method.lower()
        if method == "get":
            response = self.session.get(url=url, params=params, headers=headers)
        elif method == "post":
            response = self.session.post(url=url, json=json, data=data, files=files, headers=headers)
        elif method == "patch":
            response = self.session.patch(url=url, json=json, data=data, files=files, headers=headers)

        return response
