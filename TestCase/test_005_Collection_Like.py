import unittest
import requests
from common.mock import *
from common.readConfig import ReadConfig


class CollectionLike(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        全局使用一篇帖子，且一定执行顺序要先收藏再取消，点赞同理
        :return:
        """
        localReadConfig = ReadConfig()
        cls.addOrCancelLike = base_url + '/like/userLog/addOrCancelLike'
        cls.addCollection = base_url + '/collection/post/addCollection'
        # 随机获取一个点赞数和收藏数都为0的帖子，防止该账号由于已经操作过导致业务失败
        sql = "select id from t_post where collect_count=0 and like_count=0 and post_state=2 order by RAND() limit 1"
        db.executeSQL(sql)
        post_id = db.get_one()
        cls.headers = {'accessKey': localReadConfig.get_headers("accessKey")}
        globals()['post_id'] = post_id["id"]  # 解决在unttest框架中，testcase中间不共享变量的值
        globals()['post_id'] = '46244025413816320'  # 解决在unttest框架中，testcase中间不共享变量的值

    def setUp(self):
        """
        初始化，重置参数
        """
        self.data = {}

    def tearDown(self):
        print("请求参数：", self.data)
        print("响应数据：", self.res)

    def my_request_post(self, url):
        return requests.post(url=url, json=self.data, headers=self.headers).json()

    def test_addCollection_01(self):
        """
        收藏帖子
        step1: operation=1
        step2: 调用addCollection接口
        """
        self.data = {"operation": 1, "postId": globals()['post_id'], "topicId": "0"}
        self.res = self.my_request_post(url=self.addCollection)
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])

    def test_addCollection_02(self):
        """
        验证同一用户不能对帖子进行重复收藏
        step1: 再次执行test_addCollection_01
        """
        self.data = {"operation": 1, "postId": globals()['post_id'], "topicId": "0"}
        self.res = self.my_request_post(url=self.addCollection)
        self.assertFalse(self.res['success'])
        self.assertEqual('已收藏', self.res['desc'])

    def test_addCollection_03(self):
        """
        取消帖子收藏
        step1: operation=0
        step2: 调用addCollection接口
        """
        self.data = {"operation": 0, "postId": globals()['post_id'], "topicId": "0"}
        self.res = self.my_request_post(url=self.addCollection)
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])

    def test_addOrCancelLike_04(self):
        """
        点赞帖子
        step1: operation=1
        step2: 调用addOrCancelLike接口
        """
        self.data = {"bizType": 1, "refId": globals()['post_id'], "operation": "1"}
        self.res = self.my_request_post(url=self.addOrCancelLike)
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])

    def test_addOrCancelLike_05(self):
        """
        验证同一用户不能对帖子进行重复点赞
        step1: 再次执行test_addOrCancelLike_04
        """
        self.data = {"bizType": 1, "refId": globals()['post_id'], "operation": "1"}
        self.res = self.my_request_post(url=self.addOrCancelLike)
        self.assertFalse(self.res['success'])
        self.assertEqual('已点赞', self.res['desc'])

    def test_addOrCancelLike_06(self):
        """
        取消点赞
        step1: operation=0
        step2: 调用addOrCancelLike接口
        """
        self.data = {"bizType": 1, "refId": globals()['post_id'], "operation": "0"}
        self.res = self.my_request_post(url=self.addOrCancelLike)
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])


if __name__ == '__main__':
    unittest.main()
