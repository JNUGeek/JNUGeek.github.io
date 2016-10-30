# -*- coding: utf-8 -*-

"""查看,增加用户信息"""

import flask_restful as restful
import flask_login as login

from flask_restful import reqparse
from flask import g, session

import common.models as models
from common.error import (
        UserInfoNotFound
    )


class UserInfo(restful.Resource):
    """Get User Information."""

    @login.login_required
    def post(self):  # 添加用户信息
        parser = reqparse.RequestParser()
        parser.add_argument('student_id', type=int)
        parser.add_argument('grade', type=str)
        parser.add_argument('department', type=str)
        parser.add_argument('school', type=str)
        parser.add_argument('major', type=str)
        parser.add_argument('qq', type=str)
        parser.add_argument('introduction', type=str)
        args = parser.parse_args()

        user_info = login.current_user.user_info
        if not user_info:
            user_info = models.UserInfo(uid=login.current_user.uid)
            g.db.session.add(user_info)

        for info in args.keys():
            if not args[info]:
                continue
            setattr(user_info, info, args[info])  # 没有就放进去即user_info.info = args[info]

        g.db.session.commit()

        return {"uid": user_info.uid}

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str)

        args = parser.parse_args()

        if 'uid' not in args or not args['uid']:
            if login.current_user.is_authenticated:
                args['uid'] = login.current_user.uid
            else:
                raise UserInfoNotFound("UID is not provided")

        user_info = models.UserInfo.query.get(args['uid'])
        if not user_info and args['uid'] != login.current_user.uid:
            raise UserInfoNotFound("This user hasn't provided any information")

        result = {}

        for info in ['student_id', 'grade', 'department',
                     'school', 'major', 'qq', 'introduction']:
            result[info] = getattr(user_info, info)  # 用户信息放到result中即result[info] = user_info.info

        return result

Entry = UserInfo

