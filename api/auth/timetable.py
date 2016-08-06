# -*- coding: utf-8 -*-

"""成员提交空课表"""

import flask_restful as restful
import flask_login as login

from flask_restful import reqparse

import common.models as models


class Timetable(restful.Resource):
    """Get contacts."""
    @login.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('timetable', type=bool, action='append')
        args = parser.parse_args()

        tt = models.Timetable.query.get()
        if tt is None:
            tt = models.Timetable()
            tt = models.Timetable.query.get()

        for day in tt:
            if args['timetable'][0] is True:
                day.mon = args['timetable'][0]
            if args['timetable'][1] is True:
                day.tue = args['timetable'][1]
            if args['timetable'][2] is True:
                day.wed = args['timetable'][2]
            if args['timetable'][3] is True:
                day.thur = args['timetable'][3]
            if args['timetable'][4] is True:
                day.fri = args['timetable'][4]
            if args['timetable'][5] is True:
                day.sat = args['timetable'][5]
            if args['timetable'][6] is True:
                day.sun = args['timetable'][6]

        g.db.session.add(tt)
        g.db.session.commit()

    def get(self):
        timetable = models.Timetable.query.get()

        result = {}
        for i in range(0, 7):
            result[i] = [timetable[i].mon,
                         timetable[i].tue,
                         timetable[i].wed,
                         timetable[i].thur,
                         timetable[i].fri,
                         timetable[i].sat,
                         timetable[i].sun]

        return result

Entry = Timetable
