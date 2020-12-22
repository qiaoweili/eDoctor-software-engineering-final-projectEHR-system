"""
@reocrd_test.py consists of unlogined user test for record.py
class: RecordPostTest(unittest.TestCase)
function: test_user_unlogined(self)

"""
import unittest
import requests
import json
host = "http://127.0.0.1:6789/"
s = requests.session()
api = "/api/record/upload"
m = "post"

class RecordPostTest(unittest.TestCase):
    global s
    global api
    global m

    def test_user_unlogined(self):
        u = json.dumps({"patient_id": "account1@qq.com",
                                           "disease_name": "COVID-19",
                                           "disease_category": 1,
                                           "symptom": "Cough, Fever, Shortness of breath",
                                           "medicine": 'Unknown'})
        r = s.request(m, host + api, data=u)
        self.assertEqual(json.loads(r.text),{'code': '500', 'err_msg': 'Please login \n 请登录后进行操作', 'data': {'href': '/auth'}})

if __name__ == '__main__':
    unittest.main(verbosity=2)
