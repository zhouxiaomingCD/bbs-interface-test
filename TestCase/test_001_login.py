# import unittest
# import requests
# from common.mock import *
#
#
# class TestLogin(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.url = base_url + '/car-oauth2/uaa/oauth2.0/token'
#         cls.headers = {'client_identity': localReadConfig.get_headers("client_identity")}
#
#     def setUp(self):
#         """
#         初始化，重置用户名和密码
#         """
#         self.data = {'username': localReadConfig.get_account("username"),
#                      "password": localReadConfig.get_account("pwd")}
#         print("url：", self.url)
#         print("请求头：", self.headers)
#
#     def tearDown(self):
#         print("请求参数：", self.data)
#         print("响应数据：", self.res)
#
#     def my_request_post(self):
#         return requests.post(self.url, self.data, headers=self.headers).json()
#
#     def test_login_1(self):
#         """
#         正确用户名和密码进行登录
#         """
#         self.res = self.my_request_post()
#         status_code = self.res['statusCode']
#         message = self.res['message']
#         if '密码连续错误5次' in message:
#             return True
#         access_token = self.res['data']['access_token']
#         success = self.res['success']
#         self.assertTrue(success)
#         self.assertEqual(1000, status_code)
#         self.assertEqual('成功', message)
#         self.assertIsNotNone(access_token)
#         localReadConfig.set_headers('Authorization', access_token)
#
#     def test_login_2(self):
#         """
#         正确用户名和错误密码进行登录
#         """
#         self.data['password'] = '1234567'
#         self.res = self.my_request_post()
#         success = self.res.get('success')
#         self.assertFalse(success)
#         status_code = self.res.get('statusCode')
#         message = self.res.get('message')
#         if '密码连续错误5次' in message:
#             return True
#         self.assertEqual(2000, status_code)
#         self.assertEqual('用户名或密码错误', message)
#
#     def test_login_3(self):
#         """
#         用户名为空进行登录
#         """
#         self.data['username'] = ''
#         self.res = self.my_request_post()
#         success = self.res.get('success')
#         self.assertFalse(success)
#         status_code = self.res.get('statusCode')
#         message = self.res.get('message')
#         self.assertEqual(2000, status_code)
#         self.assertEqual('账号不能为空', message)
#
#     def test_login_4(self):
#         """
#         错误格式账号进行登录
#         """
#         self.data['username'] = 'xxx'
#         self.res = self.my_request_post()
#         success = self.res.get('success')
#         self.assertFalse(success)
#         status_code = self.res.get('statusCode')
#         message = self.res.get('message')
#         self.assertEqual(2000, status_code)
#         self.assertEqual('账号格式不正确', message)
#
#     def test_login_5(self):
#         """
#         未注册账号进行登录
#         """
#         self.data['username'] = '18226647895'
#         self.res = self.my_request_post()
#         success = self.res.get('success')
#         self.assertFalse(success)
#         status_code = self.res.get('statusCode')
#         message = self.res.get('message')
#         self.assertEqual(2000, status_code)
#         self.assertEqual('账号不存在', message)
#
#     def test_login_6(self):
#         """
#         密码为空进行登录
#         """
#         self.data['password'] = ''
#         self.res = self.my_request_post()
#         success = self.res.get('success')
#         self.assertFalse(success)
#         status_code = self.res.get('statusCode')
#         message = self.res.get('message')
#         self.assertEqual(2000, status_code)
#         self.assertEqual('密码不能为空', message)
#
#
# if __name__ == '__main__':
#     unittest.main()
