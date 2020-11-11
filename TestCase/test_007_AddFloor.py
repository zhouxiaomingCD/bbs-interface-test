import unittest
import requests
from common.mock import *
from common.readConfig import ReadConfig


class AddFloor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        localReadConfig = ReadConfig()
        cls.addFloor = base_url + '/floor/addFloor'
        cls.headers = {'accessKey': localReadConfig.get_headers("accessKey")}

    def setUp(self):
        """
        初始化，重置参数
        """
        # 随机获取一个帖子
        sql = "select id from t_post where post_state=2 ORDER BY RAND() limit 1"
        db.executeSQL(sql)
        post_id = db.get_one()["id"]
        self.data = {"content": "", "isFloorId": "", "postCreateAt": "", "postId": post_id}

    def tearDown(self):
        print("请求参数：", self.data)
        print("响应数据：", self.res)

    def my_request_post(self):
        return requests.post(url=self.addFloor, json=self.data, headers=self.headers).json()

    def test_addFloor_01(self):
        """
        发布回帖
        step1: 随机选择一篇帖子
        step2: 调用/floor/addFloor接口
        """
        self.data['content'] = random_text()
        self.data['isFloorId'] = 0
        self.data['postCreateAt'] = get_now_sec()
        self.res = self.my_request_post()
        self.assertTrue(self.res['success'])
        self.assertEqual('提交成功', self.res['desc'])

    def test_addFloor_02(self):
        """
        验证同一个用户回帖频率不能低于30s
        step1: 随机选择一篇帖子
        step2: 调用/floor/addFloor接口
        """
        self.data['content'] = random_text()
        self.data['isFloorId'] = 0
        self.data['postCreateAt'] = get_now_sec()
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('您回帖操作较频繁，请30秒后再试', self.res['desc'])


if __name__ == '__main__':
    unittest.main()
