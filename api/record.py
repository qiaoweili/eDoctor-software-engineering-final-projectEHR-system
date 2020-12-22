"""
record.py :: for dealing with medi_record form in db
classes: MedicalRecord()
"""
from lib.common.base import Base
from header import db
from flask import request, session
from api.wrapper import check_login
import datetime
import json


class MedicalRecord(Base):

    PAGE_LIMIT = 20

    @check_login
    def get(self):
        """
        for searching and showing of medical record
        used at index.html , record.html
        search to show 最新日志 recent activities @ index.html
        search to show all past medical records @ record.html
        """
        token = request.cookies.get("token", None)
        if token == session.get("token"):
            ret = []
            page = int(request.args.get("page", 1))
            direct = int(request.args.get("direct", -1))
            limit = int(request.args.get("limit", self.PAGE_LIMIT))
            disease_category = request.args.get("disease_category", "all")
            disease_name = request.args.get("disease_name", "all")
            account = session["account"]

            user = db.user.find_one({"account": account})
            if user:
                if user["u_type"] == 0 or user["u_type"] == 1:

                    if disease_category == "all":
                        disease_category_filter = ".*"
                    else:
                        disease_category_filter = ".*{}.*".format(disease_category)

                    if disease_name == "all":
                        disease_name_filter = ".*"
                    else:
                        disease_name_filter = ".*{}.*".format(disease_name)

                    if user["u_type"] == 0:
                        for i in db.medi_record.find({"patient_id": account,
                                                      "disease_category": {"$regex": disease_category_filter},
                                                      "disease_name": {"$regex": disease_name_filter}}, {"_id": 0}).sort("date", direct).skip((page - 1) * limit).limit(limit):
                            ret.append(i)
                    else:
                        for i in db.medi_record.find({"doctor_id": account,
                                                      "disease_category": {"$regex": disease_category_filter},
                                                      "disease_name": {"$regex": disease_name_filter}}, {"_id": 0}).sort("date", direct).skip((page - 1) * limit).limit(limit):
                            ret.append(i)
                    return self.api_suc(ret, ext={"count": len(ret), "page": page})
                else:
                    return self.api_fail("no permission for tbp user")
            else:
                return self.api_fail("unregistered account")

        return self.api_fail("error token")

    @check_login
    def post(self):
        """
        insert new medical record into db.medi_record.
        insertion happens at diagnose.html.
        first check account, then insert
        """
        token = request.cookies.get("token", None)
        if token == session.get("token"):
            account = session["account"]

            user = db.user.find_one({"account": account})
            if user:
                if user["u_type"] == 0 or user["u_type"] == 2:
                    print("only doctor has permission to this section")
                    return self.api_fail("no permission for patient or tbp user")

                date = datetime.datetime.now()
                # get js input
                data = json.loads(request.data)
                patient_id = data["patient_id"]


                doctor_id = account
                # gender = int(data["gender"])
                disease_name = data["disease_name"]
                disease_category = data["disease_category"]
                symptom = data["symptom"]
                medicine = data["medicine"]

                db.medi_record.insert_one({"date": date, "patient_id": patient_id,
                                           "doctor_id": doctor_id,
                                           # "gender": gender,
                                           "disease_name": disease_name,
                                           "disease_category": disease_category,
                                           "symptom": symptom,
                                           "medicine": medicine
                                           })
                return self.api_suc({"href": "/"})
            return self.api_fail("unregistered account")
        return self.api_fail("error token")
