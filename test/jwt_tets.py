import jwt
import datetime
from jwt import exceptions
import base64
SALT = 'kemUmw1zTFQL2aLH6b9FW5RH8ApmCN5Bx2F8NIfGcJc='


def create_token():
    # 构造header
    headers = {
        'alg': 'HS256'
    }
    # 构造payload
    payload = {"userId": "18810169295265792", "nickName": "1", "centerId": "760175501208715264",
               "exp": "1604010744201", "phone": "18200395978",
               "ticket": "ST-11-iGnubHhPtl6RW-NWesyjKeVT3v810"}
    result = jwt.encode(payload=payload, key=SALT,
                        algorithm="HS256", headers=headers).decode("utf-8")
    return result


if __name__ == '__main__':
    token = create_token()
    print(token)
