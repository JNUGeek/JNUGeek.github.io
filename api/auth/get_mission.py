# -*- coding: utf-8 -*-

"""成员查看任务"""


import flask_restful as restful
import flask_login as login
from flask_restful import reqparse


import common.models as models
from common.error import (
        UserInfoNotFound
    )


class GetMn(restful.Resource):

    @login.login_required
    def get(self):

        mission = models.Mission.query.filter_by\
        (uid=login.current_user.uid).order_by(models.Mission.cred_at).all()
        if mission is None:
            raise UserInfoNotFound("No missions posted.")

        result = {}
        for info in ['act_name', 'act_date', 'act_content', 'remarks']:
            result[info] = getattr(mission, info)

        return result

Entry = GetMn
