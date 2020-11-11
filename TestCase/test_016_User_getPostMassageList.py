import unittest
import requests
from common.mock import *
from common.readConfig import ReadConfig


class GetPostMassageList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        localReadConfig = ReadConfig()
        cls.url = base_url + '/message/post/getPostMassageList'
        cls.headers = {'accessKey': localReadConfig.get_headers("accessKey")}
        cls.user_id = localReadConfig.get_account("user_id")

    def setUp(self):
        """
        初始化，重置参数
        """
        self.data = {"pageIndex": 1, "pageSize": 15, "userId": self.user_id}

    def tearDown(self):
        print("请求参数：", self.data)
        print("响应数据：", self.res)

    def my_request_post(self):
        return requests.post(url=self.url, json=self.data, headers=self.headers).json()

    def test_getReminderList_01(self):
        """
        查询个人中心-我的消息-帖子通知
        step1: 读取本地存储的user_id
        step2: 调用/message/post/getPostMassageList接口
        """
        self.res = self.my_request_post()
        count = self.res['data']['count']
        li = self.res['data']['list']
        self.assertIsNotNone(count)
        self.assertIsNotNone(li)
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])
