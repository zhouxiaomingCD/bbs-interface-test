import unittest
import requests
from common.mock import *
from common.readConfig import ReadConfig


class AddFloorReply(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        localReadConfig = ReadConfig()
        cls.url = base_url + '/floor/reply/addFloorReply'
        cls.headers = {'accessKey': localReadConfig.get_headers("accessKey")}

    def setUp(self):
        """
        初始化，重置参数
        """
        # 随机获取一个帖子
        sql = "select t_floor.id from t_floor inner join t_post on t_floor.post_id=t_post.id where " \
              "t_post.post_state=2 and t_floor.floor_state=2 ORDER BY RAND() limit 1 "
        db.executeSQL(sql)
        floorId = db.get_one()["id"]
        self.data = {"content": "", "floorId": floorId}

    def tearDown(self):
        print("请求参数：", self.data)
        print("响应数据：", self.res)

    def my_request_post(self):
        return requests.post(url=self.url, json=self.data, headers=self.headers).json()

    def test_addFloorReply_01(self):
        """
        发布回帖点评
        step1: 随机选择一个楼层
        step2: 调用/floor/reply/addFloorReply接口
        """
        self.data['content'] = random_text()
        self.res = self.my_request_post()
        self.assertTrue(self.res['success'])
        self.assertEqual('提交成功', self.res['desc'])

    def test_addFloorReply_02(self):
        """
        验证同一个用户发布点评频率不能低于30s
        step1: 随机选择一个楼层
        step2: 调用/floor/reply/addFloorReply接口
        """
        self.data['content'] = random_text()
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('您回帖点评操作较频繁，请30秒后再试', self.res['desc'])


if __name__ == '__main__':
    unittest.main()
