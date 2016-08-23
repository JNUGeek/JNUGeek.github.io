# -*- coding: utf-8 -*-

"""创建新用户"""


import flask_restful as restful
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError

from flask import g
from common.utils import (
        email_type,
        phone_type,
        md5_hashed_type,
    )
from common.error import *
import common.models as models


class Account(restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('email', type=email_type)
        parser.add_argument('phone', type=phone_type)
        parser.add_argument('passwd', type=md5_hashed_type)

        args = parser.parse_args()

        new_account = models.Account(
                passwd=args['passwd'],
            )
        g.db.session.add(new_account)
        g.db.session.flush()  # 刷新数据库

        new_username = models.Credential(
                cred_type='name',  # 类型
                cred_value=args['name'],
                uid=new_account.uid
            )
        g.db.session.add(new_username)

        if args['email']:
            new_email = models.Credential(
                    cred_type='email',
                    cred_value=args['email'],
                    uid=new_account.uid
                )
            g.db.session.add(new_email)

        if args['phone']:
            new_phone = models.Credential(
                    cred_type='phone',
                    cred_value=args['phone'],
                    uid=new_account.uid
                )
            g.db.session.add(new_phone)

        try:
            g.db.session.commit()
        except IntegrityError:
            raise AccountAlreadyExists()

        return {'uid': new_account.uid}

Entry = Account

