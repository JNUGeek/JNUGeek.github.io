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
        parser.add_argument('act_name', type=str, required=True)
        parser.add_argument('act_date', type=str, required=True)
        parser.add_argument('name', type=str, action='append', required=True)
        parser.add_argument('act_content', type=str, action='append', required=True)
        parser.add_argument('remarks', type=str, action='append')

        args = parser.parse_args()

        new_mission = models.Mission()
        for info in ['act_name', 'act_date']:
            if not args[info]:
                continue
            setattr(new_mission, info, args[info])
        for (name, content, rmk) in zip(args['name'], args['act_content'], args['remarks']):
            info = models.Credential.query.filter_by(cred_type='name', cred_value=name).first()
            uid = info.uid
            # 为毛id要是字符...
            member = models.MnMember(id=str(new_mission.id), uid=uid, name=name, act_content=content, remarks=rmk)
            g.db.session.add(member)

        g.db.session.add(new_mission)
        g.db.session.commit()

        return {'id': new_mission.id}

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

Entry = Mission
