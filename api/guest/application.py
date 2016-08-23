# -*- coding: utf-8 -*-

"""游客预报名"""


import flask_restful as restful
from flask_restful import reqparse


from flask import g
from common.utils import (
        phone_type
    )
import common.models as models


class Application(restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('student_id', type=int, required=True)
        parser.add_argument('grade', type=str)
        parser.add_argument('school', type=str, required=True)
        parser.add_argument('major', type=str, required=True)
        parser.add_argument('phone', type=phone_type, required=True)
        parser.add_argument('qq', type=str)
        parser.add_argument('department', type=str, required=True)
        parser.add_argument('introduction', type=str)
        parser.add_argument('admission', type=bool)

        args = parser.parse_args()

        new_applicant = models.Applications()
        for info in args.keys():
            if not args[info]:
                continue
            setattr(new_applicant, info, args[info])
        g.db.session.add(new_applicant)
        g.db.session.commit()

        return {'id': new_applicant.id}

Entry = Application
