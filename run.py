import unittest
from common.HTMLTestRunner import HTMLTestRunner
from BeautifulReport import BeautifulReport
from unittest import TestSuite
import os
import time
from TestCase import test_014_User_getCollectionList
from TestCase.test_005_Collection_Like import CollectionLike
from common.create_auth import check_set_token
from common.mock import get_now_minute

current_path = os.getcwd()  # 获取当前路径
case_path = os.path.join(current_path, "TestCase")  # 设置用例路径
report_path = os.path.join(current_path, "Report")  # 设置报告存放路径

check_set_token()  # 查询token并写入配置文件


# 加载测试用例

def load_all_case():
    # 使用discover()方法自动匹配用例文件
    discover = unittest.defaultTestLoader.discover(case_path, pattern="test*.py")
    return discover


# def load_all_case():
#     # (模块名)但是我看源码提示是说在3.5已经移除使用，那就不用这个了
#     discover = unittest.defaultTestLoader.loadTestsFromModule(test_014_User_getCollectionList)
#     return discover


# def load_all_case():
#     # 使用类名
#     discover = unittest.defaultTestLoader.loadTestsFromTestCase(CollectionLike)  # 使用类名
#     return discover


def run():
    """
    定义测试报告，执行测试用例脚本
    :return:
    """
    # filename = os.path.join(report_path, get_time() + 'result.html')
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner(stream=fp, verbosity=2,
    #                         title='自动化测试报告',
    #                         description='测试用例执行详情')
    # result = runner.run(load_all_case())
    BeautifulReport(load_all_case()).report(description='论坛接口', filename=get_now_minute() + 'result.html',
                                            report_dir=report_path, theme='theme_candy')

    # fp.close()
    # print("总用例数：", result.testsRun)
    # print("成功：", result.success_count)
    # print("失败：", result.failure_count)
    # print("错误：", result.error_count)


if __name__ == '__main__':
    # 执行测试
    run()
