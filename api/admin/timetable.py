# -*- coding: utf-8 -*-

"""管理员查看空课表"""

import flask_restful as restful
import flask_login as login

from flask_restful import reqparse

import common.models as models


class Timetable(restful.Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user', type=str, default='')  # timetable是一个list中有list的复杂的list
        args = parser.parse_args()

        if args['user']:
            user = models.UserInfo.query.filter_by(cred_value=args['user']).first()
            uid = user.uid
            timetable = models.MyTimetable.query.get(uid)
        else:
            timetable = models.Timetable.query.get()

        result = {}
        number = []
        for num in range(10):
            number.append(num)

        for (i, cls) in zip(number, timetable):
            j = 0
            for day in ['mon', 'tue', 'wed',
                        'thur', 'fri', 'sat', 'sun']:
                result['timetable'][i][j] = getattr(cls, day)
                j += 1

        return result  # result里面的timetable对应的value也和上面的相同形式

Entry = Timetable
