# -*- coding: utf-8 -*-

"""创建新用户"""

import re

import flask_restful as restful # adds support for quickly building REST APIs
from flask_restful import reqparse # 参数解析
from sqlalchemy.exc import IntegrityError # 用来报错

from flask import g # g保存一个request的全局变量
from common.utils import (
        email_type,
        phone_type,
        md5_hashed_type,
    ) # 规定了格式
from common.error import *
import common.models as models


class Account(restful.Resource):
    # 应该是把用户数据存放到数据库
    def post(self):
        parser = reqparse.RequestParser() # 创建了请求解析对象
        parser.add_argument('name', required=True) # 把参数都加入进入
        parser.add_argument('email', type=email_type)
        parser.add_argument('phone', type=phone_type)
        parser.add_argument('passwd', type=md5_hashed_type)

        args = parser.parse_args() # 自动获取响应的数据

        new_account = models.Account( # 存放密码
                passwd = args['passwd'],
            )
        g.db.session.add(new_account) # 放到数据库
        g.db.session.flush() # 刷新数据库

        new_username = models.Credential( # 存放用户名
                cred_type = 'name', # 类型
                cred_value = args['name'], # 名字
                uid = new_account.uid # uid和Account类中的是相同
            )
        g.db.session.add(new_username) # 存到数据库

        if args['email']: # 如果填写了邮箱,把邮箱也存进去
            new_email = models.Credential(
                    cred_type = 'email',
                    cred_value = args['email'],
                    uid = new_account.uid
                )
            g.db.session.add(new_email)

        if args['phone']: # 如果填写了手机号,把手机号也存进去
            new_phone = models.Credential(
                    cred_type = 'phone',
                    cred_value = args['phone'],
                    uid = new_account.uid
                )
            g.db.session.add(new_phone)

        try:
            g.db.session.commit() # 把改动提交
        except IntegrityError:
            raise AccountAlreadyExists()

        return { 'uid': new_account.uid } # 返回一个含有uid的dict

Entry = Account

