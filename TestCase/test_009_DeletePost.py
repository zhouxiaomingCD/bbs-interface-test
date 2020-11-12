import unittest
import requests
from common.mock import *
from common.readConfig import ReadConfig


class DeletePost(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        localReadConfig = ReadConfig()
        cls.url = base_url + '/post/consumer/deletePost'
        cls.headers = {'accessKey': localReadConfig.get_headers("accessKey")}
        cls.user_id = localReadConfig.get_account("user_id")

    def setUp(self):
        """
        初始化，重置参数
        """
        self.data = {"postId": ""}
        self.res = None

    def tearDown(self):
        print("请求参数：", self.data)
        print("响应数据：", self.res)

    def my_request_post(self):
        return requests.post(url=self.url, json=self.data, headers=self.headers).json()

    def test_deletePost_01(self):
        """
        删除帖子
        step1: 随机选择一篇帖子
        step2: 调用/post/consumer/deletePost接口
        """
        sql = f"select id from t_post where post_state=2 and user_id='{self.user_id}' ORDER BY RAND() limit 1"
        db.executeSQL(sql)
        post_id = db.get_one()
        if not post_id:
            return self.skipTest("此用户暂未发布过帖子，当前用例不涉及")
        self.data['postId'] = post_id["id"]
        self.res = self.my_request_post()
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])

    def test_deletePost_02(self):
        """
        验证不能删除已删除的帖子
        step1: 随机选择一篇已删除帖子
        step2: 调用/post/consumer/deletePost接口
        """
        sql = f"select id from t_post where post_state=0 and user_id='{self.user_id}' ORDER BY RAND() limit 1"
        db.executeSQL(sql)
        post_id = db.get_one()
        if not post_id:
            return self.skipTest("该用户没有已被删除的帖子，此用例不涉及")
        self.data['postId'] = post_id["id"]
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('帖子未发布', self.res['desc'])

    def test_deletePost_03(self):
        """
        验证不能删除他人发布的帖子
        step1: 随机选择一篇他人发布的帖子
        step2: 调用/post/consumer/deletePost接口
        """
        sql = f"select id from t_post where post_state=2 and user_id!='{self.user_id}' ORDER BY RAND() limit 1"
        db.executeSQL(sql)
        post_id = db.get_one()
        self.data['postId'] = post_id["id"]
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('无权限！', self.res['desc'])

    def test_deletePost_04(self):
        """
        验证不能删除待审核的帖子
        step1: 随机选择一篇待审核的帖子
        step2: 调用/post/consumer/deletePost接口
        """
        sql = f"select id from t_post where post_state=1 and user_id='{self.user_id}' ORDER BY RAND() limit 1"
        db.executeSQL(sql)
        post_id = db.get_one()
        if not post_id:
            return self.skipTest('查询无待审核的帖子，当前用例不涉及')
        self.data['postId'] = post_id["id"]
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('帖子未发布', self.res['desc'])

    def test_deletePost_05(self):
        """
        验证不能删除加精的帖子
        step1: 随机选择一篇当前用户加精的帖子
        step2: 调用/post/consumer/deletePost接口
        """
        sql = f"select id from t_post where post_state=2 and is_high_quality=1 and user_id='{self.user_id}' ORDER BY " \
              f"RAND() limit 1"
        db.executeSQL(sql)
        post_id = db.get_one()
        if not post_id:
            return self.skipTest("查询当前用户无加精的帖子，此用例不涉及")
        self.data['postId'] = post_id["id"]
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('您的帖子已被管理员加精，请不要删除哦！', self.res['desc'])

    def test_deletePost_06(self):
        """
        验证不能删除置顶的帖子
        step1: 随机选择一篇当前用户置顶的帖子
        step2: 调用/post/consumer/deletePost接口
        """
        sql = f"select id from t_post where post_state=1 and is_toped=1 and user_id='{self.user_id}' ORDER BY RAND() " \
              f"limit 1"
        db.executeSQL(sql)
        post_id = db.get_one()
        if not post_id:
            return self.skipTest("查询当前用户无置顶的帖子，此用例不涉及")
        self.data['postId'] = post_id["id"]
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('您的帖子已被管理员置顶，请不要删除哦！', self.res['desc'])


if __name__ == '__main__':
    unittest.main()
