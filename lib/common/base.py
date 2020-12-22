import json

from flask.views import View, MethodView
from flask import make_response, request
from lib.utils import DatetimeJSONEncoder


class Base(MethodView):
    ''' Base基类 '''

    def render(self, data, output_format=None):
        callback = request.args.get("callback", False)
        if not callback:
            response = make_response(json.dumps(data, cls=DatetimeJSONEncoder))
            response.headers['Content-Type'] = 'application/json'
        else:
            response = make_response("%s(%s)" % (callback, json.dumps(data, cls=DatetimeJSONEncoder)))
            response.headers['Content-Type'] = 'application/javascript'

        return response

    def api_suc(self, data='', code=200, output_format="json", ext=None):
        ''' 按格式输出数据 '''
        data = {'code': str(code), "err_msg": "", 'data': data}
        if ext:
            for key in ext.keys():
                data[key] = ext[key]
        return self.render(data, output_format)

    def render_error(self, msg, code=500, output_format="json"):
        data = {'code': str(code), "err_msg": msg, 'data': {}}
        return self.render(data, output_format)

    def api_error(self, msg='错误输出', code=500, output_format="json"):
        return self.render_error(msg, code, output_format)

    def api_fail(self, msg="请求出错", code=500, output_format="json"):
        return self.api_error(msg, code, output_format)

    def api_args_error(self, msg="参数错误", code=1001):
        return self.api_error(msg, code)

    def api_data_existed(self, msg="数据已存在", code=1002):
        return self.api_error(msg, code)

    def api_data_noexisted(self, msg="数据不存在", code=1003):
        return self.api_error(msg, code)
