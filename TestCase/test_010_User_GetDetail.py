import unittest
import requests
from common.mock import *
from common.readConfig import ReadConfig


class GetDetail(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        localReadConfig = ReadConfig()
        cls.url = base_url + '/user/getDetail'
        cls.headers = {'accessKey': localReadConfig.get_headers("accessKey")}
        cls.user_id = localReadConfig.get_account("user_id")

    def setUp(self):
        """
        初始化，重置参数
        """
        self.data = {"id": self.user_id}

    def tearDown(self):
        print("请求参数：", self.data)
        print("响应数据：", self.res)

    def my_request_post(self):
        return requests.post(url=self.url, json=self.data, headers=self.headers).json()

    def test_getDetail_01(self):
        """
        查询登录用户个人资料
        step1: 读取本地存储的user_id
        step2: 调用/user/getDetail接口
        """
        self.res = self.my_request_post()
        createAt = self.res['data']['createAt']
        user_id = self.res['data']['id']
        imgHead = self.res['data']['imgHead']
        integrationCurrentAmount = self.res['data']['integrationCurrentAmount']
        integrationOutAmount = self.res['data']['integrationOutAmount']
        integrationTotalAmount = self.res['data']['integrationTotalAmount']
        introduction = self.res['data']['introduction']
        levelTitle = self.res['data']['levelTitle']
        loginAt = self.res['data']['loginAt']
        nickName = self.res['data']['nickName']
        self.assertIsNotNone(createAt)
        self.assertIsNotNone(user_id)
        self.assertIsNotNone(imgHead)
        self.assertIsNotNone(integrationCurrentAmount)
        self.assertIsNotNone(integrationOutAmount)
        self.assertIsNotNone(integrationTotalAmount)
        self.assertIsNotNone(introduction)
        self.assertIsNotNone(levelTitle)
        self.assertIsNotNone(loginAt)
        self.assertIsNotNone(nickName)
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])
