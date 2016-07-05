# -*- coding: utf-8 -*-

'查看,增加用户信息'

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
    def post(self): # 添加用户信息
        parser = reqparse.RequestParser()
        parser.add_argument('student_id', type=int)
        parser.add_argument('department', type=str)
        parser.add_argument('school', type=str)
        parser.add_argument('introduction', type=str)
        args = parser.parse_args()

        user_info = login.current_user.user_info # 绑定用户属性到当前用户上
        if not user_info: # 如果没有用户信息
            user_info = models.UserInfo(uid=login.current_user.uid) # 创建一个用户信息对象
            g.db.session.add(user_info) # 加到数据库

        for info in args.keys(): # 把信息放到参数里
            if not args[info]: continue # 如果有就不管
            setattr(user_info, info, args[info]) # 没有就放进去即user_info.info = args[info]

        g.db.session.commit() #提交

        return { "uid": user_info.uid }

    def get(self): # 获取用户信息
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str)
        parser.add_argument('info', type=str, action='append', required=True)
        args = parser.parse_args()

        if 'uid' not in args or not args['uid']: # 参数中没有uid
            if login.current_user.is_authenticated: # 该用户已登录
                args['uid'] = login.current_user.uid # uid加到参数中
            else:
                raise UserInfoNotFound("UID is not provided")

        user_info = models.UserInfo.query.get(args['uid']) # 从数据库中获取用户信息
        if not user_info:
            raise UserInfoNotFound("This user hasn't provided any information")

        result = {}

        for info in args["info"]:
            if info not in [ 'student_id', 'department',
                    'school', 'introduction' ]: continue
            result[info] = getattr(user_info, info) # 用户信息放到result中即result[info] = user_info.info

        return result

Entry = UserInfo

