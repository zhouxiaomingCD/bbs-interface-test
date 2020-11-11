import unittest
import requests
from common.mock import *
from common.readConfig import ReadConfig


class AddPostVote(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        localReadConfig = ReadConfig()
        cls.addPost = base_url + '/post/addPost'
        cls.headers = {'accessKey': localReadConfig.get_headers("accessKey")}
        # globals()['my_car_list'] = []  # 解决在unttest框架中，testcase中间不共享变量的值
        # globals()['currentDefaultCar_id'] = int()  # 解决在unttest框架中，testcase中间不共享变量的值

    def setUp(self):
        """
        初始化，重置参数
        """
        random_cid_tid = get_cate_top_id()
        options = [{"optionContent": random_title()} for _ in range(random.randint(3, 20))]  # 随机3-20个投票选项
        self.data = {"categoryId": random_cid_tid['categoryId'], "topicId": random_cid_tid['topicId'],
                     "title": random_title(),
                     "content": random_text(), "attachments": [],
                     "voteInfo": {"endAt": random_end_time(), "startAt": random_start_time(), "optType": 1,
                                  "optionalNum": random.randint(2, len(options)), "options": options}}
        print("请求头：", self.headers)

    def tearDown(self):
        print("请求参数：", self.data)
        print("响应数据：", self.res)

    def my_request_post(self):
        return requests.post(url=self.addPost, json=self.data, headers=self.headers).json()

    def test_addVote_01(self):
        """
        验证正常发起多选投票
        step1: 设置投票类型参数optType=1
        step2：调用addPost接口
        """
        self.data['voteInfo']["optType"] = 1
        self.res = self.my_request_post()
        self.assertTrue(self.res['success'])
        self.assertEqual('提交成功', self.res['desc'])

    def test_addVote_02(self):
        """
        验证正常发起单选投票
        step1: 设置投票类型参数optType=0
        step2：生成20个以内的投票选项
        step3：调用addPost接口
        """
        self.data['voteInfo']['optType'] = 0
        self.res = self.my_request_post()
        self.assertTrue(self.res['success'])
        self.assertEqual('提交成功', self.res['desc'])

    def test_addVote_03(self):
        """
        验证投票开始时间不能大于结束时间
        step1: 获取随机板块id和对应的主题id
        step2：生成20个以内的投票选项
        step3：开始时间设置为未来的30-60天内，结束时间设置在未来的1-30天内
        step4：调用addPost接口
        """
        start_time = datetime.datetime.strftime(
            datetime.datetime.now() + datetime.timedelta(days=random.randint(30, 60)), '%Y-%m-%d %H:%M')
        end_time = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30)),
                                              '%Y-%m-%d %H:%M')
        self.data['voteInfo']["startAt"] = start_time
        self.data['voteInfo']["endAt"] = end_time
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('投票结束时间不可早于开始时间', self.res['desc'])

    def test_addVote_04(self):
        """
        验证投票开始时间不能小于当前时间
        step1：开始时间设置为昨天，结束时间设置在未来的1-30天内
        step2：调用addPost接口
        """
        start_time = datetime.datetime.strftime(
            datetime.datetime.now() - datetime.timedelta(days=1), '%Y-%m-%d %H:%M')
        end_time = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30)),
                                              '%Y-%m-%d %H:%M')
        self.data['voteInfo']["startAt"] = start_time
        self.data['voteInfo']["endAt"] = end_time
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('投票开始时间不可早于当前时间', self.res['desc'])

    def test_addVote_05(self):
        """
        验证投票时间前后选择不能超过60天
        step1：开始时间设置为明天，结束时间设置在未来的第61天（62-1=60），边界值测试
        step2：调用addPost接口 ==>新增投票贴成功
        step3：开始时间设置为明天，结束时间设置在未来的第62天（62-1=61>60）
        step4：调用addPost接口 ==>新增投票贴失败
        """

        start_time = datetime.datetime.strftime(
            datetime.datetime.now() + datetime.timedelta(days=1), '%Y-%m-%d %H:%M')

        end_time = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=61),
                                              '%Y-%m-%d %H:%M')
        self.data['voteInfo']["startAt"] = start_time
        self.data['voteInfo']["endAt"] = end_time
        self.res = self.my_request_post()
        self.assertTrue(self.res['success'])
        self.assertEqual('提交成功', self.res['desc'])
        self.tearDown()  # 打印请求响应数据
        end_time = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=62),
                                              '%Y-%m-%d %H:%M')
        self.data['voteInfo']["endAt"] = end_time
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('投票起止时间最长间隔60天', self.res['desc'])

    def test_addVote_06(self):
        """
        验证投票最多可选项不能为负数
        step1：设置投票最多可选项为-1
        step2：调用addPost接口
        """
        self.data['voteInfo']["optionalNum"] = -1
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('最多可选数非法', self.res['desc'])

    def test_addVote_07(self):
        """
        验证多选投票输入值大于可选个数时默认为可全选
        step1：设置发送数据optionalNum为20（最多可选数为20）
        step2：调用addPost接口
        step3：连接数据库查询刚才发帖的最大可选项数量是否等于选项个数
        """
        self.data['voteInfo']["optionalNum"] = 20
        option_len = len(self.data['voteInfo']['options'])
        print("发帖选项数：", option_len)
        title = self.data['title']
        self.res = self.my_request_post()
        sql = """select optional_num from t_vote INNER JOIN t_post on t_vote.post_id =t_post.id where
        t_post.title='%s'""" % title
        print(sql)
        db.executeSQL(sql)
        result = db.get_one()
        print('数据库存放的最大可选个数：', result)
        self.assertEqual(option_len, result['optional_num'])

    def test_addVote_08(self):
        """
        验证投票帖标题不能输入为空
        step1：设置title为空
        step2：调用addPost接口
        """
        self.data['title'] = " "
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('请设置帖子名称！', self.res['desc'])

    def test_addVote_09(self):
        """
        验证投票帖内容不能输入为空
        step1：设置title为空
        step2：调用addPost接口
        """
        self.data['content'] = " "
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('请输入帖子内容！', self.res['desc'])

    def test_addVote_10(self):
        """
        验证向不存在的板块下发帖会失败
        step1：设置板块id为数据库不存在的数字
        step2：调用addPost接口
        """
        self.data['categoryId'] = 123
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('获取当前帖子所属板块信息失败!', self.res['desc'])

    def test_addVote_11(self):
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
