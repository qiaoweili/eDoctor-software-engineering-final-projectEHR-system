"""
@data_test.py consists of unlogined user test for data.py
class: UserInfo(unittest.TestCase)
function: test_user_unlogined(self)

"""
import unittest
import requests
import json
host = "http://127.0.0.1:6789/"
s = requests.session()
api = "/api/data/user"
m = "post"

class UserInfo(unittest.TestCase):
    global s
    global api
    global m

    def test_user_unlogined(self):
        u = json.dumps({"phone": '11111111111',"email": 'account1@qq.com',"age": '18',
                        "birth": '2000/01/01',"blood_type": '1',"height": '100',"weight":'100',"allergy": '1'})
        r = s.request(m, host + api, data=u)
        self.assertEqual(json.loads(r.text),{'code': '500', 'err_msg': 'Please login \n 请登录后进行操作', 'data': {'href': '/auth'}})

if __name__ == '__main__':
    unittest.main(verbosity=2)
