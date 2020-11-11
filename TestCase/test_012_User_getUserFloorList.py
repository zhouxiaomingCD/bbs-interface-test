import unittest
import requests
from common.mock import *
from common.readConfig import ReadConfig


class GetUserFloorList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        localReadConfig = ReadConfig()
        cls.url = base_url + '/post/getUserFloorList'
        cls.headers = {'accessKey': localReadConfig.get_headers("accessKey")}
        cls.user_id = localReadConfig.get_account("user_id")

    def setUp(self):
        """
        初始化，重置参数
        """
        self.data = {"timeCondition": 0, "categeryId": 0, "rankState": 1, "pageIndex": 1, "pageSize": 15}

    def tearDown(self):
        print("请求参数：", self.data)
        print("响应数据：", self.res)

    def my_request_post(self):
        return requests.post(url=self.url, json=self.data, headers=self.headers).json()

    def test_getUserFloorList_01(self):
        """
        查询个人中心-我的回复列表
        step1: 读取本地存储的user_id
        step2: 调用/post/getUserFloorList接口
        """
        self.res = self.my_request_post()
        count = self.res['data']['count']
        li = self.res['data']['list']
        self.assertIsNotNone(count)
        self.assertIsNotNone(li)
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])
