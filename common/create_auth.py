import os
from threading import Thread
import time
import requests
import redis
import common.readConfig as readConfig
import random
import platform

localReadConfig = readConfig.ReadConfig()
host = localReadConfig.get_redis("host")
password = localReadConfig.get_redis("password")
port = localReadConfig.get_redis("port")


def run_server():
    cmd = 'java -jar ./tools/demo-0.0.2-SNAPSHOT.jar'
    os.system(cmd)


def kill_java():
    """
    杀死java进程，保证程序终端顺利退出
    """
    time.sleep(20)
    if platform.system() == 'Windows':
        print('Windows系统')
        cmd1 = 'netstat -ano|findstr 8888'
        print(cmd1)
        res = os.popen(cmd1).readline()
        print(res)
        pid = res.split()[-1]
        cmd2 = 'tskill %s' % pid
        os.system(cmd2)
    if platform.system() == 'Linux':
        cmd = "kill -9 $(netstat -tlnp|grep 8888|awk  '{print $7}'|awk -F '/' '{print $1}')"
        os.system(cmd)


def create_gwt():
    """
    1、启动一个线程启用服务
    2、访问接口地址，后台自动写入redis数据库
    :return:
    """
    t1 = Thread(target=run_server)
    t2 = Thread(target=kill_java)
    t1.start()
    t2.start()
    t2.join()
    url = "http://127.0.0.1:8888/getJwts"
    res = requests.get(url)
    print(res.status_code)


def write_token(result, conn):
    key = random.choice(result).decode("utf-8")
    print(key)
    token = conn.get(key).decode("utf-8")
    print(token)
    solve_login_bug(token)
    localReadConfig.set_headers("accessKey", token)
    write_userId(token)
    print("已获取accessKey:", token)


def write_userId(token):
    import base64
    payload = token.split(".")[1]
    # 解决binascii.Error: Incorrect padding 编码bug（base64解码后的bytes长度至少为4且为4的倍数，不足部位以‘=’填充）
    missing_padding = 4 - len(payload) % 4
    if missing_padding:
        payload += '=' * missing_padding
    userInfo = eval(base64.urlsafe_b64decode(payload).decode())
    print(userInfo)
    userId = userInfo['userId']
    nickName = userInfo['nickName']
    print("操作用户：", nickName)
    localReadConfig.set_account("user_id", userId)
    localReadConfig.set_account("nickName", nickName)


def solve_login_bug(token):
    url = "https://test.os.cmiotcd.com:28443/forum/consumer/api/post/getCategoryPostList"
    data = {"categoryId": "20146121380864000", "isHighQuality": False, "pageIndex": 1, "pageSize": 20, "rankState": 1,
            "timeCondition": 0, "topicId": "23002397802635264"}
    headers = {'accesskey': token}
    requests.post(url=url, json=data, headers=headers)


def check_set_token():
    """
    1、写入redis数据库后随机读取一个token
    2、再写入token到配置config.ini
    :return:
    """
    conn = redis.Redis(host=host, port=port, password=password)
    result = conn.keys("bbs:consumerLogin_test*")
    if result:
        write_token(result, conn)
    else:
        create_gwt()
        result = conn.keys("bbs:consumerLogin_test*")  # ex代表seconds，px代表ms
        write_token(result, conn)


if __name__ == '__main__':
    check_set_token()
