import jwt
import datetime
from jwt import exceptions
import base64

SALT = 'kemUmw1zTFQL2aLH6b9FW5RH8ApmCN5Bx2F8NIfGcJc='


def get_payload(token):
    """
    根据token获取payload
    :param token:
    :return:
    """
    try:
        # 从token中获取payload【不校验合法性】
        # unverified_payload = jwt.decode(token, None, False)
        # print(unverified_payload)
        # 从token中获取payload【校验合法性】
        verified_payload = jwt.decode(token, SALT, True)
        return verified_payload
    except exceptions.ExpiredSignatureError:
        print('token已失效')
    except jwt.DecodeError:
        print('token认证失败')
    except jwt.InvalidTokenError:
        print('非法的token')


if __name__ == '__main__':
    token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9' \
           '.eyJ1c2VySWQiOiIxODgxMDE2OTI5NTI2NTc5MiIsIm5pY2tOYW1lIjoiMSIsImNlbnRlcklkIjoiNzYwMTc1NTAxMjA4NzE1MjY0IiwiZXhwIjoiMTYwNDAxMDc0NDIwMSIsInBob25lIjoiMTgyMDAzOTU5NzgiLCJ0aWNrZXQiOiJTVC0xMS1pR251YkhoUHRsNlJXLU5XZXN5aktlVlQzdjgxMCJ9.VQiTHo1V8Lp2ZU8MwzDB_lswgVJaETg7GAvEwCJMEXQ '
    payload = get_payload(token)
    print(payload)
