# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Create  : 2021/4/6 23:08
# @Update  : 2021/4/6 23:08
# @Detail  :


class CodingException(Exception):

    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message

    def __str__(self):
        return f"[CodingException] code:{self.code} message:{self.message}"

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message
