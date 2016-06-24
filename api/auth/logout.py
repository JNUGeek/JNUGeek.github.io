# -*- coding: utf-8 -*-

'实现登出'

import flask_restful as restful
import flask_login as login

from flask import session

class Logout(restful.Resource):

    @login.login_required
    def post(self):
        uid = login.current_user.uid \
                if login.current_user.is_authenticated else None

        login.logout_user()
        return { "uid": uid }

Entry = Logout

