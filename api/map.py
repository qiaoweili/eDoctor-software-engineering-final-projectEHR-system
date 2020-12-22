"""
map.py: for mapping api
"""

from api.auth import *
from api.data import *
from api.record import *

# 用户：医生，病人，第三方机构
# 医生，病人，第三方机构分别根据用户名+密码登录，每次就诊可以将当前就诊记录放入数据库，病人和医生可以浏览过往医疗记录；
# 数据库包含的是病人所有的就诊信息


def map_url(app):
    app.add_url_rule('/api/auth/login', view_func=AuthLogin.as_view("login"))
    app.add_url_rule('/api/auth/logout', view_func=AuthLogout.as_view("logout"))
    app.add_url_rule('/api/auth/register', view_func=AuthRegister.as_view("register"))

    app.add_url_rule('/api/data/user', view_func=UserInfo.as_view("user"))

    app.add_url_rule('/api/record/upload', view_func=MedicalRecord.as_view("record_upload"))
    app.add_url_rule('/api/record/search', view_func=MedicalRecord.as_view("record_search"))

