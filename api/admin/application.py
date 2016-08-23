# -*- coding: utf-8 -*-

"""管理员查看预报名"""


import flask_restful as restful

import common.models as models
from common.error import (
        UserInfoNotFound
    )


class Application(restful.Resource):

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
                    applicant[info] = None
                applicant[info] = getattr(user, info)
            result[user.id] = applicant

        return result

Entry = Application  # 能不能共用Entry呢?
