# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Create  : 2021/4/6 20:46
# @Update  : 2021/4/6 20:46
# @Detail  : requests.

from coding_api.common.exception import CodingException
import requests


class ApiRequests:
    _protocol = 'https'
    _endpoiot = '.coding.net'

    def __init__(self, team_name, token):
        self._url = f'{self._protocol}://{team_name}{self._endpoiot}'
        self.headers = {'Authorization': f'token {token}'}

    def send_request(self, action, data: dict):
        reqest_path = f'/open-api?Action={action}'
        data.update({
            'Action': action
        })
        try:
            response = requests.post(f'{self._url}{reqest_path}', json=data, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            raise CodingException('NetworkError', str(e))
        else:
            return response
