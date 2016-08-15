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
        parser.add_argument('uid', type=str, required=True)
        parser.add_argument('content', type=str, required=True)

        args = parser.parse_args()

        new_notification = models.Notification()
        for info in args.keys():
            if not args[info]:
                continue
            setattr(new_notification, info, args[info])
        g.db.session.add(new_notification)
        g.db.session.flush()

        return {'id': new_notification.id}

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        args = parser.parse_args()

        notification = models.Notification.query.get(args['id'])
        if notification is None:
            raise UserInfoNotFound("No notifications posted.")

        result = {}
        for info in ['title', 'department', 'name', 'content']:
            result[info] = getattr(notification, info)

        return result

Entry = Notify
