import unittest
import requests
from common.mock import *
from common.readConfig import ReadConfig


class StartVote(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        localReadConfig = ReadConfig()
        cls.addPost = base_url + '/vote/startVote'
        cls.headers = {'accessKey': localReadConfig.get_headers("accessKey")}
        cls.user_id = localReadConfig.get_account("user_id")

    def setUp(self):
        """
        初始化，重置参数
        """
        self.data = {"optionIds": [], "postId": "", "voteId": ""}
        print("请求头：", self.headers)

    def tearDown(self):
        print("请求参数：", self.data)
        print("响应数据：", self.res)

    def my_request_post(self):
        return requests.post(url=self.addPost, json=self.data, headers=self.headers).json()

    def get_all_voted_ids(self, opt_type):
        """
        1、拿到目前所有可以投票的帖子id
        2、拿到当前用户已经投过的帖子id
        :param opt_type: 0-单选投票 1-多选投票
        :return:
        """
        print('查询所有投票未结束的帖子，包括没有人投过票的')
        sql1 = "select v2.post_id,v1.user_id from t_vote_log v1 right JOIN (select post_id from t_vote,t_post where " \
               "t_post.id=t_vote.post_id and opt_type=%d and start_at<NOW() and end_at>NOW() and post_state=2) v2 on " \
               "v1.post_id = v2.post_id " % opt_type
        print(sql1)
        db.executeSQL(sql1)
        li_for_all = list(set(i["post_id"] for i in db.get_all()))
        # print(li_for_all)
        print('查询投票未结束但该用户投过票的帖子')
        sql2 = f"select post_id from ({sql1}) v3 where v3.user_id ='{self.user_id}'"
        print(sql2)
        db.executeSQL(sql2)
        li_for_voted = [i["post_id"] for i in db.get_all()]
        # print(li_for_voted)
        return li_for_all, li_for_voted

    def test_startVote_01(self):
        """
        验证进行单选投票
        step1: 数据库查询所有投票还未结束的帖子
        step2：数据库查询该登录用户已经投过票的帖子
        step3：取两个结果的差集作为该用户可投票的帖子列表
        step4：随机选择一篇帖子的任意一个选项
        step5：调用/vote/startVote结果进行投票
        """
        li_for_all, li_for_voted = self.get_all_voted_ids(0)
        post_ids = list(set(li_for_all) ^ set(li_for_voted))  # 列表求差得到可以投票的帖子
        choose_post_id = random.choice(post_ids)
        print('获取该帖子的所有选项id和投票id')
        sql3 = f"select id,vote_id from t_vote_option where post_id='{choose_post_id}'"
        print(sql3)
        db.executeSQL(sql3)
        result = db.get_all()
        # print(result)
        option_ids = [i["id"] for i in result]
        vote_id = result[0]["vote_id"]
        self.data["optionIds"] = [random.choice(option_ids)]
        self.data["postId"] = choose_post_id
        self.data["voteId"] = vote_id
        self.res = self.my_request_post()
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])

    def test_startVote_02(self):
        """
        验证选项和帖子不匹配会投票失败
        step1: 数据库查询所有投票还未结束的帖子
        step2：数据库查询该登录用户已经投过票的帖子
        step3：取两个结果的差集作为该用户可投票的帖子列表
        step4：随机获取其他帖子的任意一个选项
        step5：调用/vote/startVote结果进行投票
        """
        li_for_all, li_for_voted = self.get_all_voted_ids(0)
        post_ids = list(set(li_for_all) ^ set(li_for_voted))  # 列表求差得到可以投票的帖子
        if not post_ids:
            print("已没有可供该用户投票的帖子")
            self.res = None
            return
        choose_post_id = random.choice(post_ids)
        print('获取其他可投票帖子的所有选项id和投票id')
        sql3 = f"select id,vote_id from t_vote_option where post_id!='{choose_post_id}'"
        print(sql3)
        db.executeSQL(sql3)
        result = db.get_all()
        # print(result)
        option_ids = [i["id"] for i in result]
        vote_id = result[0]["vote_id"]
        self.data["optionIds"] = [random.choice(option_ids)]
        self.data["postId"] = choose_post_id
        self.data["voteId"] = vote_id
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('数据错误', self.res['desc'])

    def test_startVote_03(self):
        """
        验证用户不能进行重复投票
        step1: 数据库查询所有投票还未结束的帖子
        step2：数据库查询该登录用户已经投过票的帖子
        step3：随机获取step2结果的帖子的任意一个选项
        step4：调用/vote/startVote结果进行投票
        """
        li_for_all, li_for_voted = self.get_all_voted_ids(0)
        if not li_for_voted:
            print("该用户暂时没有参与过任何投票")
            self.res = None
            return
        choose_post_id = random.choice(li_for_voted)
        print('获取该帖子的所有选项id和投票id')
        sql3 = f"select id,vote_id from t_vote_option where post_id='{choose_post_id}'"
        print(sql3)
        db.executeSQL(sql3)
        result = db.get_all()
        # print(result)
        option_ids = [i["id"] for i in result]
        vote_id = result[0]["vote_id"]
        self.data["optionIds"] = [random.choice(option_ids)]
        self.data["postId"] = choose_post_id
        self.data["voteId"] = vote_id
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('用户已经投过票', self.res['desc'])

    def test_startVote_04(self):
        """
        验证单选投票用户不能投两个选项
        step1: 数据库查询所有投票还未结束的帖子
        step2：数据库查询该登录用户已经投过票的帖子
        step3：取两个结果的差集作为该用户可投票的帖子列表
        step4：随机选择一篇帖子的任意两个选项
        step5：调用/vote/startVote结果进行投票
        """
        li_for_all, li_for_voted = self.get_all_voted_ids(0)
        post_ids = list(set(li_for_all) ^ set(li_for_voted))  # 列表求差得到可以投票的帖子
        if not post_ids:
            print("已没有可供该用户投票的帖子")
            self.res = None
            return
        choose_post_id = random.choice(post_ids)
        print('获取该帖子的所有选项id和投票id')
        sql3 = f"select id,vote_id from t_vote_option where post_id='{choose_post_id}'"
        print(sql3)
        db.executeSQL(sql3)
        result = db.get_all()
        # print(result)
        option_ids = [i["id"] for i in result]
        vote_id = result[0]["vote_id"]
        self.data["optionIds"] = random.sample(option_ids, 2)
        self.data["postId"] = choose_post_id
        self.data["voteId"] = vote_id
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('超过最大投票数', self.res['desc'])

    def test_startVote_05(self):
        """
        验证用户进行多选投票
        step1: 数据库查询所有投票还未结束的多选投票帖子
        step2：数据库查询该登录用户已经投过票的帖子
        step3：取两个结果的差集作为该用户可投票的帖子列表
        step4：查询出该帖子的所有选项和最多可选数
        step5：随机选择一篇帖子的随机多个选项
        step6：调用/vote/startVote结果进行投票
        """
        li_for_all, li_for_voted = self.get_all_voted_ids(1)
        post_ids = list(set(li_for_all) ^ set(li_for_voted))  # 列表求差得到可以投票的帖子
        if not post_ids:
            print("已没有可供该用户投票的帖子")
            self.res = None
            return
        choose_post_id = random.choice(post_ids)
        print('获取该帖子的所有选项id和投票id')
        sql3 = f"select v1.id,v1.vote_id,v2.optional_num from t_vote_option v1,t_vote v2 where v2.id=v1.vote_id and" \
               f" v1.post_id='{choose_post_id}' "
        print(sql3)
        db.executeSQL(sql3)
        result = db.get_all()
        print(result)
        option_ids = [i["id"] for i in result]
        vote_id = result[0]["vote_id"]
        optional_num = result[0]["optional_num"]
        self.data["optionIds"] = random.sample(option_ids, random.randint(1, optional_num))
        self.data["postId"] = choose_post_id
        self.data["voteId"] = vote_id
        self.res = self.my_request_post()
        self.assertTrue(self.res['success'])
        self.assertEqual('操作成功', self.res['desc'])

    def test_startVote_06(self):
        """
        验证多选投票投票数不能大于最多可选项数
        step1: 数据库查询所有投票还未结束的多选投票帖子
        step2：数据库查询该登录用户已经投过票的帖子
        step3：取两个结果的差集作为该用户可投票的帖子列表
        step4：查询出该帖子的所有选项和最多可选数(如果该帖子为全选，则此条用例忽略)
        step5：随机选择一篇帖子的随机多个选项
        step6：调用/vote/startVote结果进行投票
        """
        li_for_all, li_for_voted = self.get_all_voted_ids(1)
        post_ids = list(set(li_for_all) ^ set(li_for_voted))  # 列表求差得到可以投票的帖子
        if not post_ids:
            print("已没有可供该用户投票的帖子")
            self.res = None
            return
        choose_post_id = random.choice(post_ids)
        print('获取该帖子的所有选项id和投票id')
        sql3 = f"select v1.id,v1.vote_id,v2.optional_num from t_vote_option v1,t_vote v2 where v2.id=v1.vote_id and" \
               f" v1.post_id='{choose_post_id}' "
        print(sql3)
        db.executeSQL(sql3)
        result = db.get_all()
        print(result)
        option_ids = [i["id"] for i in result]
        vote_id = result[0]["vote_id"]
        optional_num = result[0]["optional_num"]
        if optional_num == len(option_ids):
            print("该贴子为全选，此条用例忽略")
            self.res = None
            return
        self.data["optionIds"] = random.sample(option_ids, optional_num + 1)
        self.data["postId"] = choose_post_id
        self.data["voteId"] = vote_id
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('超过最大投票数', self.res['desc'])

    def test_startVote_07(self):
        """
        验证多选投票选项不能重复
        step1: 数据库查询所有投票还未结束的多选投票帖子
        step2：数据库查询该登录用户已经投过票的帖子
        step3：取两个结果的差集作为该用户可投票的帖子列表
        step4：查询出该帖子的所有选项和最多可选数(如果该帖子为全选，则此条用例忽略)
        step5：构造两个重复选项
        step6：调用/vote/startVote结果进行投票
        """
        li_for_all, li_for_voted = self.get_all_voted_ids(1)
        post_ids = list(set(li_for_all) ^ set(li_for_voted))  # 列表求差得到可以投票的帖子
        if not post_ids:
            print("已没有可供该用户投票的帖子")
            self.res = None
            return
        choose_post_id = random.choice(post_ids)
        print('获取该帖子的所有选项id和投票id')
        sql3 = f"select v1.id,v1.vote_id,v2.optional_num from t_vote_option v1,t_vote v2 where v2.id=v1.vote_id and" \
               f" v1.post_id='{choose_post_id}' "
        print(sql3)
        db.executeSQL(sql3)
        result = db.get_all()
        print(result)
        option_ids = [i["id"] for i in result]
        vote_id = result[0]["vote_id"]
        self.data["optionIds"] = [option_ids[0], [option_ids[1]]]
        self.data["postId"] = choose_post_id
        self.data["voteId"] = vote_id
        self.res = self.my_request_post()
        self.assertFalse(self.res['success'])
        self.assertEqual('选项ID不合法！', self.res['desc'])


if __name__ == '__main__':
    unittest.main()
