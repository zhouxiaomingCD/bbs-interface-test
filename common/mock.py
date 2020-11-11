from faker import Faker
import random
from common.DBClient import db
from common.readConfig import ReadConfig
import datetime
import time

fake = Faker(locale="zh_CN")
localRead = ReadConfig()
base_url = localRead.get_http("base_url")


def random_title():
    return fake.sentence()


def random_phone():
    return fake.phone_number()


def random_name():
    return fake.name()


def random_text():
    return fake.text()


def random_eq_sn():
    return str(random.randint(1000000, 9999999))


def random_car_number():
    char0 = '京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽赣粤青藏川宁琼'
    char1 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'  # 车牌号中没有I和O，可自行百度
    char2 = '1234567890'
    len0 = len(char0) - 1
    len1 = len(char1) - 1
    len2 = len(char2) - 1
    code = ''
    index0 = random.randint(1, len0)
    index1 = random.randint(1, len1)
    code += char0[index0]
    code += char1[index1]
    for _ in range(1, 6):
        index2 = random.randint(1, len2)
        code += char2[index2]
    return code


def now_timestamp():
    return int(datetime.datetime.now().timestamp() * 1000)


def get_category_id():
    sql = """SELECT id as categoryId FROM t_category  where parent_id!=0"""

    # 执行SQL语句
    db.executeSQL(sql)
    category_id_list = db.get_all()
    return category_id_list


def get_cate_top_id():
    """
    获取堆随机板块id和对应的主题id
    :return:
    """
    print(get_category_id())
    categoryId = random.choice(get_category_id())['categoryId']
    sql = """SELECT category_id as categoryId,ID as topicId FROM t_post_topic  where category_id=%d and is_del =1""" % categoryId

    # 执行SQL语句
    db.executeSQL(sql)
    data_list = db.get_all()
    # print(data_list)
    if not data_list:
        data = {"categoryId": categoryId, "topicId": 0}
    else:
        data = random.choice(data_list)
    # print("板块id和主题id",data)
    return data
    # return cursor.fetchall()


def random_start_time():
    """
    生产随机10分钟内的开始时间
    :return:
    """
    new_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(1, 10))
    start_time = datetime.datetime.strftime(new_time, '%Y-%m-%d %H:%M')
    return start_time


def random_end_time():
    """
    生成随机60天内的结束时间
    :return:
    """
    new_time = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 60))
    end_time = datetime.datetime.strftime(new_time, '%Y-%m-%d %H:%M')
    return end_time


def get_my_userid():
    import base64
    token = localReadConfig.get_headers("accessKey").split(".")[1]
    pay_load = eval(base64.b64decode(token).decode("utf-8"))
    user_id = pay_load['userId']
    return user_id


def get_now_minute():
    """
    返回当前时间格式化信息
    :return:
    """
    # now = time.strftime('%Y-%m-%d %H_%M_%S')  # 获取当前时间，并且格式化为字符串
    now = time.strftime('%Y-%m-%d')  # 获取当前时间，并且格式化为字符串
    return now


def get_now_sec():
    """
    返回当前时间格式化信息
    :return:
    """
    now = time.strftime('%Y-%m-%d %H_%M_%S')  # 获取当前时间，并且格式化为字符串
    return now


if __name__ == '__main__':
    print(get_my_userid())
