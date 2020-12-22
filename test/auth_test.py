"""
@auth_test.py consists of unit tests for auth.py
class: UserRegistration(unittest.TestCase), UserLogin(unittest.TestCase)
function: test_email_valid(),test_account_exist(),test_password_valid(), test_sex_valid(),test_phone_valid(),test_check_password()

"""

import unittest
import requests
import json
import random

host = "http://127.0.0.1:6789/"
s = requests.session()
api_reg = "/api/auth/register"
m = "post"
api_log = "/api/auth/login"

class UserRegistration(unittest.TestCase):
    global s
    global api_reg
    global m

    def test_email_valid(self):
        u = json.dumps({'account':'accountabc','password':'12345678',
                        'name':'tester','sex':0,'birth':'2000/01/01',
                        'phone':'11111111111', "u_type": 0})
        r = s.request(m, host + api_reg, data=u)
        self.assertEqual(json.loads(r.text),{'code': '500', 'err_msg': 'account id is not valid e-mail address', 'data': {}})

    def test_account_exist(self):
        u1 = json.dumps({'account':'account1@qq.com','password':'12345678',
                          'name':'testera','sex':0,'birth':'2000/01/01',
                          'phone':'11111111111', "u_type": 0})
        u2 = json.dumps({'account':'account1@qq.com','password':'12345679',
                          'name':'testerb','sex':0,'birth':'2000/01/01',
                          'phone':'11111111111', "u_type": 0})
        r2 = s.request(m, host + api_reg, data=u2)
        self.assertEqual(json.loads(r2.text),{'code': '500', 'err_msg': 'account id has already been registered', 'data': {}})


    def test_password_valid(self):
        u1 = json.dumps({'account':str(random.randrange(10000, 100000)) + "@qq.com",'password':'12345',  # password too short
                          'name':'tester','sex':0,'birth':'2000/01/01',
                          'phone':'11111111111', "u_type": 0})
        u2 = json.dumps({'account':str(random.randrange(10000, 100000)) + "@qq.com",'password':'123456789012345678901', # password too short
                          'name':'tester','sex':0,'birth':'2000/01/01',
                          'phone':'11111111111', "u_type": 0})
        r1 = s.request(m, host + api_reg, data=u1)
        r2 = s.request(m, host + api_reg, data=u2)
        self.assertEqual(json.loads(r1.text),{'code': '500', 'err_msg': 'invalid password', 'data': {}})
        self.assertEqual(json.loads(r2.text),{'code': '500', 'err_msg': 'invalid password', 'data': {}})

    def test_sex_valid(self):
        u1 = json.dumps({'account':str(random.randrange(10000, 100000)) + "@qq.com",'password':'12345678',
                          'name':'tester','sex':2,'birth':'2000/01/01',
                          'phone':'11111111111', "u_type": 0})
        u2 = json.dumps({'account':str(random.randrange(10000, 100000)) + "@qq.com",'password':'12345678',
                          'name':'tester','sex':0,'birth':'2000/01/01',
                          'phone':'11111111111', "u_type": 0})
        u3 = json.dumps({'account':str(random.randrange(10000, 100000)) + "@qq.com",'password':'12345678',
                          'name':'tester','sex':1,'birth':'2000/01/01',
                          'phone':'11111111111', "u_type": 0})
        r1 = s.request(m, host + api_reg, data=u1)
        r2 = s.request(m, host + api_reg, data=u2)
        r3 = s.request(m, host + api_reg, data=u3)
        self.assertEqual(json.loads(r1.text),{'code': '500', 'err_msg': 'invalid sex', 'data': {}})
        self.assertEqual(json.loads(r2.text),{'code': '200', 'err_msg': '', 'data': {'href': '/auth'}})
        self.assertEqual(json.loads(r3.text),{'code': '200', 'err_msg': '', 'data': {'href': '/auth'}})

    def test_phone_valid(self):
        u1 = json.dumps({'account':str(random.randrange(10000, 100000)) + "@qq.com",'password':'12345678',
                          'name':'tester','sex':0,'birth':'2000/01/01',
                          'phone':'123456789', "u_type": 0}) # illegal
        u2 = json.dumps({'account':str(random.randrange(10000, 100000)) + "@qq.com",'password':'12345678',
                          'name':'tester','sex':0,'birth':'2000/01/01',
                          'phone':'1234567', "u_type": 0}) # illegal
        u3 = json.dumps({'account':str(random.randrange(10000, 100000)) + "@qq.com",'password':'12345678',
                          'name':'tester','sex':0,'birth':'2000/01/01',
                          'phone':'1234567890', "u_type": 0}) #illegal
        u4 = json.dumps({'account':str(random.randrange(10000, 100000)) + "@qq.com",'password':'12345678',
                          'name':'tester','sex':0,'birth':'2000/01/01',
                          'phone':'12345678901', "u_type": 0}) # ok phone number
        u5 = json.dumps({'account': str(random.randrange(10000, 100000)) + "@qq.com", 'password': '12345678',
                         'name': 'tester', 'sex': 0, 'birth': '2000/01/01',
                         'phone': '12345678', "u_type": 0})  # ok phone number
        r1 = s.request(m, host + api_reg, data=u1)
        r2 = s.request(m, host + api_reg, data=u2)
        r3 = s.request(m, host + api_reg, data=u3)
        r4 = s.request(m, host + api_reg, data=u4)
        r5 = s.request(m, host + api_reg, data=u5)
        self.assertEqual(json.loads(r1.text),{'code': '500', 'err_msg': 'invalid phone', 'data': {}})
        self.assertEqual(json.loads(r2.text),{'code': '500', 'err_msg': 'invalid phone', 'data': {}})
        self.assertEqual(json.loads(r3.text),{'code': '500', 'err_msg': 'invalid phone', 'data': {}})
        self.assertEqual(json.loads(r4.text),{'code': '200', 'err_msg': '', 'data': {'href': '/auth'}})
        self.assertEqual(json.loads(r5.text),{'code': '200', 'err_msg': '', 'data': {'href': '/auth'}})



class UserLogin(unittest.TestCase):
    global s
    global api_log
    global m

    def test_check_password(self):
        u1 = json.dumps({'account': 'account1@qq.com', 'password': '12345678'})
        r1 = s.request(m, host + api_log, data=u1) #success
        u2 = json.dumps({'account': 'account1@qq.com', 'password': '87654321'})
        r2 = s.request(m, host + api_log, data=u2)
        self.assertEqual(json.loads(r1.text)['code'],'200') # error password
        self.assertEqual(json.loads(r2.text)['err_msg'],'error password')


if __name__ == '__main__':
    unittest.main(verbosity=2)
