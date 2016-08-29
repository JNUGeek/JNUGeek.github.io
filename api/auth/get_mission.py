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

        mission = models.MnMember.query.filter_by\
        (uid=login.current_user.uid).order_by(models.MnMember.id).all()
        if mission is None:
            raise UserInfoNotFound("No missions posted.")

        result = {}
        end_mn = []
        last_mn = []
        for mn in mission:
            id = getattr(mn, 'id')
            this_mn = models.Mission.query.get(id)
            if getattr(this_mn, 'end') is False:
                last_mn.append(getattr(this_mn, 'act_name'))
            else:
                end_mn.append(getattr(this_mn, 'act_name'))
        result['end'] = end_mn
        result['last'] = last_mn

        return result

Entry = GetMn
