# -*- coding: utf-8 -*-

"""游客预报名"""


import flask_restful as restful
from flask_restful import reqparse


from flask import g
from common.utils import (
        phone_type
    )
import common.models as models
from common.error import (
        UserInfoNotFound
    )


class Application(restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()  # 创建了请求解析对象
        parser.add_argument('name', required=True)  # 把参数都加入进入
        parser.add_argument('student_id', type=int)
        parser.add_argument('grade', type=str)
        parser.add_argument('school', type=str)
        parser.add_argument('major', type=str)
        parser.add_argument('phone', type=phone_type)
        parser.add_argument('qq', type=str)
        parser.add_argument('department', type=str)
        parser.add_argument('introduction', type=str)
        parser.add_argument('admission', type=bool)

        args = parser.parse_args()  # 自动获取响应的数据

        new_applicant = models.Applications()
        for info in args.keys():
            if not args[info]:
                continue
            setattr(new_applicant, info, args[info])
        g.db.session.add(new_applicant)
        g.db.session.flush()

        return {'id': new_applicant.id}

    def get(self):
        application = models.Applications.query.get()
        if application is None:
            raise UserInfoNotFound("No new applications")

        applicant = {}
        result = {}
        for user in application:
            for info in ['name', 'student_id', 'grade', 'department',
                         'school', 'major', 'qq', 'introduction']:
                if user.info is None:
                    application[info] = None
                applicant[info] = getattr(user, info)
            result[user.id] = applicant

        return result

Entry = Application
