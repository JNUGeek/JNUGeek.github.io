# -*- coding: utf-8 -*-

"""管理员查看预报名"""


import flask_restful as restful
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError
import common.models as models
from flask import g
from common.utils import (
        phone_type
    )
from common.error import *


class Application(restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, action='append', required=True)
        parser.add_argument('student_id', action='append', type=int)
        parser.add_argument('grade', action='append', type=str)
        parser.add_argument('school', action='append', type=str)
        parser.add_argument('major', action='append', type=str)
        parser.add_argument('phone', action='append', type=phone_type, required=True)
        parser.add_argument('qq', action='append', type=str)
        parser.add_argument('department', action='append', type=str)
        parser.add_argument('introduction', action='append', type=str)

        args = parser.parse_args()

        for i in range(len(args['student_id'])):
            application = models.Applications.query.filter_by(student_id=args['student_id'][i]).first()
            if application:
                setattr(application, 'admission', True)
            new_account = models.Account(
                passwd=args['student_id'][i],  # 学号是默认密码
            )
            g.db.session.add(new_account)
            g.db.session.flush()

            new_username = models.Credential(
                cred_type='name',
                cred_value=args['name'][i],
                uid=new_account.uid
            )
            g.db.session.add(new_username)

            if args['phone']:
                new_phone = models.Credential(
                    cred_type='phone',
                    cred_value=args['phone'][i],
                    uid=new_account.uid
                )
                g.db.session.add(new_phone)

            new_info = models.UserInfo(uid=new_account.uid)
            for info in ['student_id', 'grade', 'department',
                         'school', 'major', 'qq', 'introduction']:
                if args[info]:
                    setattr(new_info, info, args[info][i])
            g.db.session.add(new_info)

        try:
            g.db.session.commit()
        except IntegrityError:
            raise AccountAlreadyExists()

        return ''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('giveup', type=bool, default=False)
        args = parser.parse_args()

        application = models.Applications.query.filter_by(admission=False).all()
        if application is None:
            raise UserInfoNotFound("No new applications")

        if args['giveup']:
            for user in application:
                g.db.session.delete(user)
            g.db.session.commit()
            return ''

        result = {}
        for user in application:
            applicant = {}
            for info in ['name', 'student_id', 'grade', 'department',
                         'school', 'major', 'qq', 'introduction']:
                if getattr(user, info) is None:
                    applicant[info] = None
                applicant[info] = getattr(user, info)
            result[getattr(user, 'id')] = applicant

        return result  # 复杂dict,dict中含有dict

Entry = Application  # 能不能共用Entry呢?
