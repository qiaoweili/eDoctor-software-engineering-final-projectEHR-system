"""
check login right at the beginning.
redirect to login page if not login yet.
"""
from flask import session, make_response, request
from functools import wraps
from lib.utils import DatetimeJSONEncoder
import json


def check_login(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get("account"):
            ret = func(*args, **kwargs)
            return ret
        else:
            callback = request.args.get("callback", False)
            if not callback:
                response = make_response(json.dumps({"code": "500", "err_msg": "Please login \n 请登录后进行操作", "data": {"href": "/auth"}}, cls=DatetimeJSONEncoder))
                response.headers['Content-Type'] = 'application/json'
            else:
                response = make_response("%s(%s)" % (callback, json.dumps({"code": "500", "err_msg": "Please login \n 请登录后进行操作", "data": {"href": "/auth"}}, cls=DatetimeJSONEncoder)))
                response.headers['Content-Type'] = 'application/javascript'
            return response

    return inner
