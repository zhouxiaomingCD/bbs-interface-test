import unittest
import requests
from common.mock import *
from common.readConfig import ReadConfig


class AddPost(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        localReadConfig = ReadConfig()
        cls.addPost = base_url + '/post/addPost'
        cls.headers = {'accessKey': localReadConfig.get_headers("accessKey")}

    def setUp(self):
        """
        初始化，重置参数
        """
        random_cid_tid = get_cate_top_id()
        self.data = {"categoryId": random_cid_tid['categoryId'], "topicId": random_cid_tid['topicId'],
                     "title": random_title(),
                     "content": random_text(), "attachments": []}
        print("请求头：", self.headers)

    def tearDown(self):
        print("请求参数：", self.data)
        print("响应数据：", self.res)

    def my_request_post(self):
        return requests.post(url=self.addPost, json=self.data, headers=self.headers).json()

    def test_addPost_01(self):
        """
        验证正常发布帖子
        step1: 选择随机板块及对应的主题
        step1: 输入标题和内容
        step3：调用addPost接口
        """
        self.res = self.my_request_post()
        self.assertTrue(self.res['success'])
        self.assertEqual('提交成功', self.res['desc'])

    def test_addPost_02(self):
        """
        验证普通帖标题不能输入为空
        step1：设置title为空
        step2：调用addPost接口
        """
        self.data['title'] = " "
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('请设置帖子名称！', self.res['desc'])

    def test_addPost_03(self):
        """
        验证普通帖内容不能输入为空
        step1：设置title为空
        step2：调用addPost接口
        """
        self.data['content'] = " "
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('请输入帖子内容！', self.res['desc'])

    def test_addPost_04(self):
        """
        验证向不存在的板块下发帖会失败
        step1：设置板块id为数据库不存在的数字
        step2：调用addPost接口
        """
        self.data['categoryId'] = 123
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('获取当前帖子所属板块信息失败!', self.res['desc'])

    def test_addPost_05(self):
        """
        验证向不存在的主题下发帖会失败
        step1：设置主题id为数据库不存在的数字
        step2：调用addPost接口
        """
        self.data['topicId'] = 123
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('板块和主题信息不匹配！', self.res['desc'])


if __name__ == '__main__':
    unittest.main()
