# -*- coding: utf-8 -*-

"""管理员修改查看预报名时间"""


import flask_restful as restful
from flask_restful import reqparse
import common.models as models
from flask import g
from common.error import (
        UserInfoNotFound
    )


class Application(restful.Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start', type=str)
        parser.add_argument('end', type=str)
        args = parser.parse_args()

        time = models.ApplyTime.query.first()
        if time is None:
            time = models.ApplyTime()

        setattr(time, 'start', args['start'])
        setattr(time, 'end', args['end'])

        g.db.session.add(time)
        g.db.session.commit()

        return ''

    def get(self):
        time = models.ApplyTime.query.first()

        result = dict()

        if time is None:
            time = models.ApplyTime()

        result['start'] = getattr(time, 'start')
        result['end'] = getattr(time, 'end')

        return result

Entry = Application  # 能不能共用Entry呢?
