import unittest
import requests
from common.mock import *
from common.readConfig import ReadConfig


class GetCollectionList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        localReadConfig = ReadConfig()
        cls.getCollectionList_p = base_url + '/collection/post/getCollectionList'
        cls.getCollectionList_c = base_url + '/collection/category/getCollectionList'
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

    def my_request_post(self, url):
        return requests.post(url=url, json=self.data, headers=self.headers).json()

    def test_getCollectionList_01(self):
        """
        查询个人中心-我的收藏-帖子收藏
        step1: 读取本地存储的user_id
        step2: 调用/collection/post/getCollectionList接口
        """
        self.res = self.my_request_post(self.getCollectionList_p)
        count = self.res['data']['count']
        li = self.res['data']['list']
        self.assertIsNotNone(count)
        self.assertIsNotNone(li)
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])

    def test_getCollectionList_02(self):
        """
        查询个人中心-我的收藏-板块收藏
        step1: 读取本地存储的user_idc
        step2: 调用/collection/category/getCollectionList接口
        """
        self.res = self.my_request_post(self.getCollectionList_c)
        count = self.res['data']['count']
        li = self.res['data']['list']
        self.assertIsNotNone(count)
        self.assertIsNotNone(li)
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])
