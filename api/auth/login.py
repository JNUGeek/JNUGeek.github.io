# -*- coding: utf-8 -*-

'实现登录'

import flask_restful as restful
import flask_login as login

from flask_restful import reqparse
from flask import g

from common.models import Credential, Account
from common.utils import (
        email_type,
        phone_type,
        md5_hashed_type,
    )
from common.error import (
        AtLeastOneOfArguments,
        CredentialNotFound,
        PasswordIncorrect,
    )


class Login(restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid')
        parser.add_argument('name')
        parser.add_argument('email', type=email_type)
        parser.add_argument('phone', type=phone_type)
        parser.add_argument('passwd', type=md5_hashed_type, default="")
        parser.add_argument('remember_me', type=bool, default=False)
        args = parser.parse_args()

        account = None

        if args['uid']:  # 如果有uid,也就是用户名
            account = Account.query.get(args['uid'])
        else:
            # 如果有name就创建name类型,没有name就创建email以此类推
            # 任意一种都可以当作用户名
            cred_type = \
                'name' if args['name'] else \
                'email' if args['email'] else \
                'phone' if args['phone'] else ''  # \是用来防止判断条件这一行过长
            cred = Credential.query.get(
                    (cred_type, args[cred_type]))
            if not cred.account:
                raise CredentialNotFound(cred_type, args[cred_type])
            account = cred.account  # 存放个人信息

        if not account:
            raise AtLeastOneOfArguments(['uid', 'name', 'email', 'phone'])

        if account.passwd.lower() != args['passwd'].lower():  # 检查密码对不对
            raise PasswordIncorrect()

        login.login_user(account, remember=args['remember_me'])  # 这里是让用户登录

        return {"uid": account.uid}

Entry = Login

