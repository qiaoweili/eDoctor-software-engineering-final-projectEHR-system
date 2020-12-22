"""
auto batch registration 批量生成账号
"""
import requests
import json
import random

host = "http://127.0.0.1:6789/"

s = requests.session()

name_map = ["joe",
            "kris",
            "tomas",
            "ford",
            "linda"]


def req(api, m="get", b=""):
    global s
    r = s.request(m, host + api, data=b)
    print(json.loads(r.text))


if __name__ == "__main__":
    num = 20

    for i in range(num):
        account = str(random.randrange(10000, 100000)) + "@qq.com"
        passwd = str(random.randrange(100000, 1000000))
        name = name_map[random.randint(a=0, b=len(name_map)-1)]
        sex = random.randint(0, 1)
        birth = str(random.randrange(10000, 100000))
        phone = str(random.randrange(10000000000, 13000000000))
        u_type = 0
        req("/api/auth/register", m="post", b=json.dumps({"account": account,
                                                          "password": passwd,
                                                          "name": name,
                                                          "sex": sex,
                                                          "birth": birth,
                                                          "phone": phone,
                                                          "u_type": u_type}))
