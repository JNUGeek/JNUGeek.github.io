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
        parser.add_argument('name', type=str, required=True)
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
                passwd=args['student_id'],  # 学号是默认密码
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

        users = models.Account.query.all()
        if users is None:
            raise UserInfoNotFound("No member exists")

        members = {}
        result = {}
        for user in users:
            for info in ['name', 'phone']:
                member = models.Credential.query.filter_by(uid=getattr(user, 'uid'), cred_type=info).first()
                if member is None:
                    members[info] = None
                else:
                    members[info] = member.cred_value

        for user in users:
            member_info = models.UserInfo.query.filter_by(uid=getattr(user, 'uid')).first()
            for info in ['student_id', 'grade', 'department',
                         'school', 'major', 'qq', 'introduction']:
                try:
                    getattr(member_info, info)
                except AttributeError as e:
                    continue
                members[info] = getattr(member_info, info)
            member = models.Credential.query.filter_by(uid=getattr(user, 'uid'), cred_type='name').first()
            result[member.cred_value] = members

        return result  # 两层dict

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('student_id', type=str)
        args = parser.parse_args()

        user = models.UserInfo.query.filter_by(student_id=args['student_id']).first()
        id = user.uid
        account = models.Account.query.get(id)
        cre = models.Credential.query.filter_by(uid=id).all()
        cre.append(user)
        cre.append(account)

        for member in cre:
            g.db.session.delete(member)
        g.db.session.commit()

        return ''

Entry = Member
