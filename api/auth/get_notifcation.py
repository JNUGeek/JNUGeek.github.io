# -*- coding: utf-8 -*-

"""成员查看通知"""


import flask_restful as restful
import flask_login as login


import common.models as models
from common.error import (
        UserInfoNotFound
    )


class GetNoti(restful.Resource):

    @login.login_required
    def get(self):

        notification = models.Notification.query.filter_by\
        (uid=login.current_user.uid).order_by(models.Notification.cred_at).add()
        if notification is None:
            raise UserInfoNotFound("No notifications posted.")

        result = {}
        for info in ['title', 'content']:
            result[info] = getattr(notification, info)

        return result

Entry = GetNoti
