# -*- coding: utf-8 -*-

"""管理员查看发送任务"""


import flask_restful as restful
import flask_login as login
from flask_restful import reqparse


from flask import g
import common.models as models
from common.error import (
        UserInfoNotFound
    )


class Mission(restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        # 这里只考虑了一行的情况,实际情况可能有多行,有点问题
        parser.add_argument('act_name', type=str, required=True)
        parser.add_argument('act_date', type=str, required=True)
        parser.add_argument('uid', type=str, required=True)
        parser.add_argument('act_content', type=str, required=True)
        parser.add_argument('remarks', type=str, default='')

        args = parser.parse_args()  # 自动获取响应的数据

        new_mission = models.Mission()
        for info in args.keys():
            if not args[info]:
                continue
            setattr(new_mission, info, args[info])
        g.db.session.add(new_mission)
        g.db.session.flush()

        return {'id': new_mission.id}

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

Entry = Mission
