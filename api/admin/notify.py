# -*- coding: utf-8 -*-

"""管理员查看发送通知"""


import flask_restful as restful
from flask_restful import reqparse


from flask import g
import common.models as models
from common.error import (
        UserInfoNotFound
    )


class Notify(restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('department', type=str, required=True)
        parser.add_argument('members', type=str, action='append', required=True)
        parser.add_argument('content', type=str, required=True)

        args = parser.parse_args()

        new_notification = models.Notification()
        id = new_notification.id
        for info in args.keys():
            if not args[info] or info == 'members':
                continue
            setattr(new_notification, info, args[info])

        if args['department'] == '其他':
            for member in args['members']:
                user = models.UserInfo.query.filter_by(name=member).first()
                info = models.Credential.query.filter_by(uid=user.uid, cred_type='name').first()
                name = info.cred_value
                noti_member = models.NotiMember(id=id, uid=user.uid, name=name)
                g.db.session.add(noti_member)
        else:
            members = models.UserInfo.query.filter_by(department=args['department']).all()
            for user in members:
                uid = getattr(user, 'uid')
                info = models.Credential.query.filter_by(uid=uid, cred_type='name').first()
                name = info.cred_value
                noti_member = models.NotiMember(id=id, uid=uid, name=name)
                g.db.session.add(noti_member)

        g.db.session.add(new_notification)
        g.db.session.commit()

        return {'id': new_notification.id}

    def get(self):
        notifications = models.Notification.query.order_by(models.Notification.cred_at).all()

        result = {}
        detail = {}
        for noti in notifications:
            id = getattr(noti, 'id')
            for info in ['title', 'department', 'content']:
                detail[info] = getattr(noti, info)
                if getattr(noti, info) == '其他':
                    detail['member'] = []
                    members = models.NotiMember.query.filter_by(id=id).all()
                    for member in members:
                        detail['member'].append(getattr(member, 'name'))
            result[id] = detail

        return result

Entry = Notify
