# -*- coding: utf-8 -*-

"""管理员查看预报名"""


import flask_restful as restful
from flask_restful import reqparse
import common.models as models
from common.error import (
        UserInfoNotFound
    )


class Application(restful.Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('giveup', type=bool, default='False')
        args = parser.parse_args()

        application = models.Applications.query.get()
        if application is None:
            raise UserInfoNotFound("No new applications")

        if args['give']:
            for user in application:
                g.db.session.delete(user)
            g.db.session.commit()

        applicant = {}
        result = {}
        for user in application:
            for info in ['name', 'student_id', 'grade', 'department',
                         'school', 'major', 'qq', 'introduction']:
                if user.info is None:
                    applicant[info] = None
                applicant[info] = getattr(user, info)
            result[user.id] = applicant

        return result  # 复杂dict,dict中含有dict

Entry = Application  # 能不能共用Entry呢?
