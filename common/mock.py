from faker import Faker
import random
from common.DBClient import db
from common.readConfig import ReadConfig
import datetime
import time

fake = Faker(locale="ja_JP")
"""
ar_EG- Arabic (Egypt)  阿拉伯语 - 埃及
ar_PS- Arabic (Palestine)阿拉伯语 - 巴勒斯坦
ar_SA- Arabic (Saudi Arabia)阿拉伯语 - 沙特阿拉伯
bg_BG- Bulgarian  保加利亚语 - 保加利亚
cs_CZ- Czech   捷克语 - 捷克
de_DE- German  德语 - 德国
dk_DK- Danish  丹麦语 - 丹麦
el_GR- Greek  希腊语 - 希腊
en_AU- English (Australia)  英语 - 澳大利亚
en_CA- English (Canada)  英语 - 加拿大
en_GB- English (Great Britain)  英语 - 英国
en_US- English (United States) 英语 - 美国
es_ES- Spanish (Spain)  西班牙语 - 西班牙
es_MX- Spanish (Mexico)  西班牙语- 墨西哥
et_EE- Estonian  爱沙尼亚语 - 爱沙尼亚
fa_IR- Persian (Iran)  波斯语 - 伊朗
fi_FI- Finnish  芬兰语 - 芬兰
fr_FR- French  法语 - 法国
hi_IN- Hindi  印地语 - 印度
hr_HR- Croatian  克罗地亚语 - 克罗地亚
hu_HU- Hungarian  匈牙利语 - 匈牙利
hy_AM- Armenian 亚美尼亚语 - 亚美尼亚
it_IT- Italian 意大利语 - 意大利
ja_JP- Japanese  日语 - 日本
ko_KR- Korean  朝鲜语 - 韩国
ka_GE- Georgian (Georgia) 格鲁吉亚语 - 格鲁吉亚
lt_LT- Lithuanian  立陶宛语 - 立陶宛
lv_LV- Latvian拉脱维亚语 - 拉脱维亚
ne_NP- Nepali尼泊尔语 - 尼泊尔
nl_NL- Dutch (Netherlands)  德语 - 荷兰
no_NO- Norwegian  挪威语 - 挪威
pl_PL- Polish  波兰语 - 波兰
pt_BR- Portuguese (Brazil)  葡萄牙语 - 巴西
pt_PT- Portuguese (Portugal)  葡萄牙语 - 葡萄牙
ru_RU- Russian  俄语 - 俄国
sl_SI- Slovene 斯诺文尼亚语 - 斯诺文尼亚
sv_SE- Swedish  瑞典语 - 瑞典
tr_TR- Turkish  土耳其语 - 土耳其
uk_UA- Ukrainian  乌克兰语 - 乌克兰
zh_CN- Chinese (China)  （简体中文）
zh_TW- Chinese (Taiwan) （繁体中文）
"""
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
    print(random_text())
