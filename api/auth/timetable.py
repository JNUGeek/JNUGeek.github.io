# -*- coding: utf-8 -*-

"""成员提交空课表"""

import flask_restful as restful
import flask_login as login
from flask import g
from flask_restful import reqparse

import common.models as models


class Timetable(restful.Resource):
    @login.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('timetable', type=int, action='append')  # timetable是一个list
        args = parser.parse_args()

        tt = models.Timetable.query.all()
        mytt = []
        for i in range(10):
            mytt.append(models.MyTimetable(uid=login.current_user.uid))
        if tt is None:
            for i in range(10):
                i = models.Timetable()
            tt = models.Timetable.query.all()

        number = []
        for num in range(10):
            number.append(num)

        for (i, cls, user) in zip(number, tt, mytt):
            j = 0
            for day in ['mon', 'tue', 'wed',
                        'thur', 'fri', 'sat', 'sun']:
                if args['timetable'][i*7 + j]:
                    value = getattr(cls, day) + 1
                    getattr(cls, day, value)
                    setattr(user, day, 1)
                j += 1

        for cls in tt:
            g.db.session.add(cls)
        for cls in mytt:
            g.db.session.add(cls)
        g.db.session.commit()

        return ''

    def get(self):
        timetable = models.Timetable.query.all()

        result = {}
        number = []
        for num in range(10):
            number.append(num)

        for (i, cls) in zip(number, timetable):
            j = 0
            for day in ['mon', 'tue', 'wed',
                        'thur', 'fri', 'sat', 'sun']:
                result['timetable'][i*7 + j] = getattr(cls, day)
                j += 1

        return result  # result里面的timetable对应的value也和上面的相同形式

Entry = Timetable
