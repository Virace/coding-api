# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Create  : 2021/4/6 20:28
# @Update  : 2021/4/6 20:28
# @Detail  : repos. 代码托管
import json
import copy
from dataclasses import dataclass
from coding_api.common.http.request import ApiRequests
from coding_api.common.exception import CodingException

from typing import List, Optional, Tuple, Union
import typing


# def formatter(text: str):
#     words = text.split('_')
#     return ''.join([word.title() for word in words])

def formatter(text: str):
    res = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            res.append("_")
        res.append(char)
    return ''.join(res).lower()


@dataclass
class Depot:
    """
    Name	String	仓库名称
    HttpsUrl	String	https 的 url 路径
    SshUrl	String	ssh 的 url 路径
    Id	Integer	仓库 id
    VcsType	String	仓库类型
    """
    name: str
    https_url: str
    ssh_url: str
    id: str
    vcs_type: str

    @staticmethod
    def load(data: dict):
        return Depot(**{formatter(key): value for key, value in data.items()})


@dataclass
class DepotData:
    depos: Optional[List[Depot]] = None

    @staticmethod
    def load(data: dict):
        this = DepotData()
        setattr(this, 'depos', [Depot.load(item) for item in data['Depots']])
        return this


@dataclass
class GitTag:
    tag_name: str
    message: str

    @staticmethod
    def load(data: dict):
        return GitTag(**{formatter(key): value for key, value in data.items()})


def dict2repo_obj(obj, data: dict) -> Union[Depot, GitTag]:
    this = copy.deepcopy(obj)
    for key in Depot.__annotations__.keys():
        setattr(this, key, data[formatter(key)])
    return this


class RepoClient:

    def __init__(self, request: ApiRequests, project_id: int):
        self.request = request
        self.project_id = project_id

    def _request(self, action, data=None) -> Tuple[dict, int]:
        if data is None:
            data = {}
        data.update({'ProjectId': self.project_id})
        response = self.request.send_request(action, data)
        try:
            data = response.json()
            request_id = data['Response']['RequestId']
            other_data = data['Response']
            if 'Error' in other_data:
                raise CodingException(other_data['Error']['Code'], other_data['Error']['Message'])
            del other_data['RequestId']
        except json.JSONDecodeError or KeyError:
            raise CodingException('Response Error', response.text)
        else:
            return other_data, request_id

    def create_git_depot(self, project_name: str) -> Tuple[int, int]:
        """
        创建代码仓库
        :param project_name:
        :return:
        """
        data, request_id = self._request('CreateGitDepot', {"DepotName": project_name})
        return data['DepotId'], request_id

    def delete_git_depot(self, depot_id: int) -> int:
        """
        删除代码仓库
        :param depot_id:
        :return:
        """
        _, request_id = self._request('DeleteGitDepot', {"DepotId": depot_id})
        return request_id

    def create_git_commit_note(self, depot_id, notes_ref, commit_sha, note, commit_message):
        """
        创建提交注释
        :param depot_id:
        :param notes_ref:
        :param commit_sha:
        :param note:
        :param commit_message:
        :return:
        """
        _, request_id = self._request('DeleteGitDepot', {
            "DepotId": depot_id,
            "NotesRef": notes_ref,
            "CommitSha": commit_sha,
            "Note": note,
            "CommitMessage": commit_message
        })
        return request_id

    def describe_project_depot_info_list(self) -> Tuple[DepotData, int]:
        """
        查询项目下仓库信息列表
        :return:
        """
        data, request_id = self._request('DescribeProjectDepotInfoList')
        try:
            pd = DepotData.load(data['DepotData'])
        except Exception as e:
            raise CodingException('Unknown Error', str(e))
        else:
            return pd, request_id

    def describe_git_tags(self, depot_id) -> Tuple[List[GitTag], int]:
        """
        查询仓库所有标签
        :param depot_id:
        :return:
        """
        data, request_id = self._request('DescribeGitTags', {"DepotId": depot_id})
        try:
            pd = [GitTag.load(item) for item in data['GitTags']]
        except Exception as e:
            raise CodingException('Unknown Error', str(e))
        else:
            return pd, request_id

    def describe_git_tags_by_branch(self, branch, depot_id):

        data, request_id = self._request('DescribeGitTagsByBranch', {"DepotId": depot_id, "Branch": branch})
        try:
            pd = data['Tags']
        except Exception as e:
            raise CodingException('Unknown Error', str(e))
        else:
            return pd, request_id

    def describe_git_tag(self, depot_id, tag_name) -> Tuple[GitTag, int]:
        """
        查询指定标签
        :param depot_id:
        :param tag_name:
        :return:
        """
        data, request_id = self._request('DescribeGitTag', {"DepotId": depot_id, "TagName": tag_name})
        try:
            pd = GitTag.load(data['GitTag'])
        except Exception as e:
            raise CodingException('Unknown Error', str(e))
        else:
            return pd, request_id
