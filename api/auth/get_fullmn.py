# -*- coding: utf-8 -*-

"""成员查看详细任务"""


import flask_restful as restful
import flask_login as login
from flask_restful import reqparse


from flask import g
import common.models as models
from common.error import (
        UserInfoNotFound
    )


class GetFullMission(restful.Resource):

    @login.login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        args = parser.parse_args()

        mission = models.Mission.query.filter_by\
        (id=args['id']).order_by(models.Mission.cred_at).first()
        if mission is None:
            raise UserInfoNotFound("No missions posted.")

        result = {}
        result['act_name'] = mission.act_name
        result['act_date'] = mission.act_date
        names = []
        contents = []
        remarks = []
        members = models.MnMember.query.filter_by(id=args['id']).all()
        for member in members:
            names.append(getattr(member, 'name'))
            contents.append(getattr(member, 'act_content'))
            remarks.append(getattr(member, 'remarks'))
        result['names'] = names
        result['contents'] = contents
        result['remarks'] = remarks

        return result  # dict中含list

Entry = GetFullMission
