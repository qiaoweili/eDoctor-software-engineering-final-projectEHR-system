"""
data.py : for index.html
classes: UserInfo(Base)
"""
from lib.common.base import Base
from header import db
from flask import request, session
from api.wrapper import check_login
import json


class UserInfo(Base):
    """
    for User form in database.

    """
    @check_login
    def get(self):
        """
        check if the account exist.
        if exist, return userinfo of that account
        """
        token = request.cookies.get("token", None)
        if token == session.get("token"):
            account = session["account"]
            user = db.user.find_one({"account": account}, {"_id": 0, "password": 0})
            if user:
                return self.api_suc(user)
            else:
                return self.api_fail("user not found")

        return self.api_fail("auth failed, error token")

    @check_login
    def post(self):
        """
        for updating personal profile @ profile.html
        check token first.
        find the account in db, then update userinfo in USER form in db
        """
        token = request.cookies.get("token", None)
        if token == session.get("token"):
            account = session["account"]

            user = db.user.find_one({"account": account})
            if user:
                data = json.loads(request.data)
                phone = data["phone"]
                email = data["email"]
                age = int(data["age"])
                birth = data["birth"]
                blood_type = data["blood_type"]
                height = float(data["height"])
                weight = float(data["weight"])
                allergy = data["allergy"]

                data_to_be_updated = {"phone": phone,
                                      "email": email,
                                      "age": age,
                                      "birth": birth,
                                      "blood_type": blood_type,
                                      "height": height,
                                      "weight": weight,
                                      "allergy": allergy}
                db.user.update_one({"account": account}, {"$set": data_to_be_updated})
                return self.api_suc({"href": "/"})
            return self.api_fail("unregistered account")
        return self.api_fail("error token")
