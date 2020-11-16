import unittest
import requests
from common.mock import *


class GetPostRankList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.getPostRankList = base_url + '/post/getPostRankList'

    def setUp(self):
        """
        初始化，重置参数
        """
        self.data = {"rankState": 5, "pageIndex": 1, "pageSize": 10}

    def tearDown(self):
        print("请求参数：", self.data)
        print("响应数据：", self.res)

    def my_request_post(self):
        return requests.post(url=self.getPostRankList, json=self.data).json()

    def test_getPostRankList_01(self):
        """
        查看热门帖子
        step1: 设置rankState=1
        step1: 调用getPostRankList接口
        step3：获取数据库查询结果
        step4：比较接口返回数据和数据库查询数据是否一致，排序是否一致
        """
        self.data["rankState"] = 1
        self.res = self.my_request_post()
        sql = "select id from t_post where post_state = 2 order by hot_count desc limit 10"
        db.executeSQL(sql)
        result = db.get_all()
        post_id_list_db = [str(post['id']) for post in result]
        li = self.res['data']["list"]
        post_id_list_res = [post['id'] for post in li]
        print("数据库查询结果：", result)
        print("接口返回结果：", post_id_list_res)
        self.assertEqual(post_id_list_db, post_id_list_res)

    def test_getPostRankList_02(self):
        """
        查看最多浏览帖子
        step1: 设置rankState=2
        step1: 调用getPostRankList接口
        step3：获取数据库查询结果
        step4：比较接口返回数据和数据库查询数据是否一致，排序是否一致
        """
        self.data["rankState"] = 2
        self.res = self.my_request_post()
        sql = "select id from t_post where post_state = 2 order by read_count desc limit 10"
        db.executeSQL(sql)
        result = db.get_all()
        post_id_list_db = [str(post['id']) for post in result]
        li = self.res['data']["list"]
        post_id_list_res = [post['id'] for post in li]
        print("数据库查询结果：", result)
        print("接口返回结果：", post_id_list_res)
        self.assertEqual(post_id_list_db, post_id_list_res)

    def test_getPostRankList_03(self):
        """
        查看最多回复帖子
        step1: 设置rankState=3
        step1: 调用getPostRankList接口
        step3：获取数据库查询结果
        step4：比较接口返回数据和数据库查询数据是否一致，排序是否一致
        """
        self.data["rankState"] = 3
        self.res = self.my_request_post()
        sql = "select id from t_post where post_state = 2 order by floor_count desc limit 10"
        db.executeSQL(sql)
        result = db.get_all()
        post_id_list_db = [str(post['id']) for post in result]
        li = self.res['data']["list"]
        post_id_list_res = [post['id'] for post in li]
        print("数据库查询结果：", result)
        print("接口返回结果：", post_id_list_res)
        self.assertEqual(post_id_list_db, post_id_list_res)

    def test_getPostRankList_04(self):
        """
        查看最最新发布帖子
        step1: 设置rankState=4
        step1: 调用getPostRankList接口
        step3：获取数据库查询结果
        step4：比较接口返回数据和数据库查询数据是否一致，排序是否一致
        """
        self.data["rankState"] = 4
        self.res = self.my_request_post()
        sql = "select id from t_post where post_state = 2 order by new_recent desc limit 10"
        db.executeSQL(sql)
        result = db.get_all()
        post_id_list_db = [str(post['id']) for post in result]
        li = self.res['data']["list"]
        post_id_list_res = [post['id'] for post in li]
        print("数据库查询结果：", result)
        print("接口返回结果：", post_id_list_res)
        self.assertEqual(post_id_list_db, post_id_list_res)

    def test_getPostRankList_05(self):
        """
        查看最新回复帖子
        step1: 设置rankState=5
        step1: 调用getPostRankList接口
        step3：获取数据库查询结果
        step4：比较接口返回数据和数据库查询数据是否一致，排序是否一致
        """
        self.data["rankState"] = 5
        self.res = self.my_request_post()
        sql = "select id from t_post where post_state = 2 order by last_reply_at desc,id desc limit 10"
        db.executeSQL(sql)
        result = db.get_all()
        post_id_list_db = [str(post['id']) for post in result]
        li = self.res['data']["list"]
        post_id_list_res = [post['id'] for post in li]
        print("数据库查询结果：", result)
        print("接口返回结果：", post_id_list_res)
        self.assertEqual(post_id_list_db, post_id_list_res)


if __name__ == '__main__':
    unittest.main()
