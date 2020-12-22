"""
@auth.py is used for authentication
class: AuthRegister(Base), AuthLogin(Base), AuthLogout(Base)
all classes have two functions: get(self), post(self)
@staticmethod:
check_password_valid(p), check_sex_valid(sex), check_phone_valid(phone)

"""

import os
# sys.path.append(os.getcwd())
import json
import hashlib
import validators
from lib.common.base import Base
from header import db
from flask import request, session


class AuthRegister(Base):
    """
    AuthRegister: for registration authentication
    EMP_KEY, TBP_KEY: key for usertype doctor and third-party to register.
    """
    EMP_KEY = "ucanguessEMPkkkey"
    TBP_KEY = "ucantguessTBPkkkey"

    def get(self):
        """
            get():not supported in register

        """
        return self.api_error("Get is not support in action: register")

    def post(self):
        """
            post(): insert registration input value into databse

        """
        data = json.loads(request.data)
        account = data.get("account", None)

        if not validators.email(account) == True:
            return self.api_fail("account id is not valid e-mail address")

        user = db.user.find_one({"account": account})
        if user:
            return self.api_fail("account id has already been registered")

        password = data.get("password", None)
        if not self.check_password_valid(password):
            return self.api_fail("invalid password")

        name = data.get("name", None)
        if not self.check_name_valid(name):
            return self.api_fail("invalid name")

        sex = int(data.get("sex", None))
        if not self.check_sex_valid(sex):
            return self.api_fail("invalid sex")

        birth = data.get("birth", None)
        if not self.check_birth_valid(birth):
            return self.api_fail("invalid birth")

        phone = data.get("phone", None)
        if not self.check_phone_valid(phone):
            return self.api_fail("invalid phone")
        phone = phone.replace(" ", "")

        u = int(data.get("u_type", 0))

        if u == 1:
            emp_key = data.get("key", None)
            if not emp_key == self.EMP_KEY:
                return self.api_fail("error emp key")
        elif u == 2:
            tbp_key = data.get("key", None)
            if not tbp_key == self.TBP_KEY:
                return self.api_fail("error tbp key")

        db.user.insert_one({"account": account, "password": password, "u_type": u,
                            "name": name,
                            "sex": sex,
                            "birth": birth,
                            "phone": phone})
        return self.api_suc({"href": "/auth"})

    @staticmethod
    def check_password_valid(p):
        """
        password length:  6 <= len(p) <= 20
        """
        if 6 <= len(p) <= 20:
            return True
        return False

    # @staticmethod
    # def check_name_valid(name):
    #     # todo
    #     return True

    @staticmethod
    def check_sex_valid(sex):
        if sex == 0 or sex == 1:
            return True
        return False

    # @staticmethod
    # def check_birth_valid(birth):
    #     # todo
    #     return True

    @staticmethod
    def check_phone_valid(phone):
        """
        phone number length fixed: 8 or 11 digits
        """
        phone = phone.replace(" ", "")
        if phone.startswith("+"):
            s = phone.split("-")[1]
        else:
            s = phone

        if len(s) == 8 or len(s) == 11:
            return True
        return False


class AuthLogin(Base):
    """
    AuthLogin for checking login
    """
    def get(self):
        """
            get(): not support for login

        """
        return self.api_error("Get is not support in action: login")

    def post(self):
        """
            post(): load input, check acount with info in database;
            if login success, set session,
            generate token and store in cookie

        """
        data = json.loads(request.data)
        account = data.get("account", None)

        if account in session:
            return self.api_error("account has already been login")

        password = data.get("password", None)

        user = db.user.find_one({"account": account, "password": password})

        if not user:
            return self.api_fail("error password")

        session["u_type"] = user["u_type"]
        session["account"] = account
        h = hashlib.md5(os.urandom(24))
        session["token"] = h.hexdigest()

        resp = self.api_suc({"account": account, "token": session["token"], "href": "/"})
        resp.set_cookie("token", session["token"], max_age=12 * 3600)
        return resp


class AuthLogout(Base):
    """
    AuthLogout: for logging out

    """
    def get(self):
        """
         get(): not supported for logout
        """
        return self.api_error("Get is not support in action: logout")

    def post(self):
        """
        post(): first check account and status,
            if valid: clear session, delete cookie
        """
        token = request.cookies.get("token", None)
        if "account" in session and "token" in session:
            if session.get("token", None) == token:
                session.clear()
                resp = self.api_suc({"href": "/auth"})
                resp.delete_cookie("token")
                return resp
            return self.api_fail("error user info")
        return self.api_fail("not login or expired, please login again")
