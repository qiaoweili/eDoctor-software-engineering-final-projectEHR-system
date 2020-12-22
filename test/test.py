"""
login/logout auto test
"""

import requests
import json

host = "http://127.0.0.1:6789/"

s = requests.session()


def req(api, m="get", b=""):
    global s
    r = s.request(m, host + api, data=b)
    print(r.text)
    return json.loads(r.text)


if __name__ == "__main__":
    d = req("api/auth/login", m="post", b=json.dumps({"account": "1234", "password": "123"}))
    req("api/auth/logout", m="post", b=json.dumps({"account": "1234", "token": d["data"]["token"]}))
