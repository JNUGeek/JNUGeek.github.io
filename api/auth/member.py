# -*- coding: utf-8 -*-

"""管理员添加查看成员"""


import flask_restful as restful
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError

from flask import g
from common.utils import (
        phone_type
    )
from common.error import *
import common.models as models


class Member(restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('student_id', type=int)
        parser.add_argument('grade', type=str)
        parser.add_argument('school', type=str)
        parser.add_argument('major', type=str)
        parser.add_argument('phone', type=phone_type)
        parser.add_argument('qq', type=str)
        parser.add_argument('department', type=str)
        parser.add_argument('introduction', type=str)

        args = parser.parse_args()

        new_account = models.Account(
                passwd=args['student_id'],
            )
        g.db.session.add(new_account)
        g.db.session.flush()

        new_username = models.Credential(
                cred_type='name',
                cred_value=args['name'],
                uid=new_account.uid
            )
        g.db.session.add(new_username)

        if args['phone']:
            new_phone = models.Credential(
                    cred_type='phone',
                    cred_value=args['phone'],
                    uid=new_account.uid
                )
            g.db.session.add(new_phone)

        new_info = models.UserInfo(uid=new_account.uid)
        for info in ['student_id', 'grade', 'department',
                     'school', 'major', 'qq', 'introduction']:
            if args[info]:
                setattr(new_info, info, args[info])
        g.db.session.add(new_info)

        try:
            g.db.session.commit()
        except IntegrityError:
            raise AccountAlreadyExists()

        return {'uid': new_account.uid}

    def get(self):
        users = models.Account.query.get()
        if users is None:
            raise UserInfoNotFound("No member exists")

        members = {}
        result = {}
        for user in users:
            for info in ['name', 'phone']:
                member = models.Credential.query.filter_by(uid=user.uid, cred_type=info).first()
                if member.cred_type is None:
                    members[info] = None
                members[info] = member.cred_value
            result[user.id] = members
        for user in users:
            member_info = models.UserInfo.query.get(user.uid)
            for info in ['student_id', 'grade', 'department',
                         'school', 'major', 'qq', 'introduction']:
                if user.info is None:
                    members[info] = None
                members[info] = getattr(member_info, info)
            result[user.id] = members

        return result

Entry = Member
