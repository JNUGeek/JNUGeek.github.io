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

        notification = models.NotiMember.query.filter_by\
         (uid=login.current_user.uid).order_by(models.NotiMember.cred_at).all()
        if notification is None:
            raise UserInfoNotFound("No notifications posted.")

        result = {}
        for noti in notification:
            title = getattr(noti, 'title')
            result[title] = []
            nt = models.Notification.query.filter_by(title=title).first()
            for info in ['title', 'content']:
                result[info].append(getattr(nt, info))

        return result  # dict中包含list

Entry = GetNoti
