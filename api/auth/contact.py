# -*- coding: utf-8 -*-

"""成员查看联系人"""

import flask_restful as restful
import flask_login as login

from flask_restful import reqparse

import common.models as models
from common.error import (
        UserInfoNotFound
    )


class Contact(restful.Resource):
    """Get contacts."""
    @login.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        return {'name': args['name']}

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('info', type=str, action='append', required=True)
        args = parser.parse_args()

        if 'name' not in args or not args['name']:
            raise UserInfoNotFound("Name is not provided")

        contacts_info = models.Credential.query.filter_by(cred_value=args['name']).first()
        if not contacts_info:
            raise UserInfoNotFound("This user hasn't provided any information")

        uid = contacts_info.uid
        contacts_info = models.UserInfo.query.get(uid)

        result = {}

        for info in args["info"]:
            if info not in ['student_id', 'grade', 'department',
                            'school', 'major', 'qq', 'introduction']:
                continue
            result[info] = getattr(contacts_info, info)

        return result

Entry = Contact
