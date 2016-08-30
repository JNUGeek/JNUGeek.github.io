# -*- coding: utf-8 -*-

"""管理员删除成员"""


import flask_restful as restful
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError

from flask import g
from common.utils import (
        phone_type
    )
from common.error import *
import common.models as models


class DeleteMember(restful.Resource):

    def get(self):
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

Entry = DeleteMember
