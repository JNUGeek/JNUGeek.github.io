# -*- coding: utf-8 -*-

from flask import g, current_app

db = g.db

import uuid  # UUID 的目的，是让分布式系统中的所有元素，都能有唯一的辨识资讯，而不需要透过中央控制端来做辨识资讯的指定。
import datetime


class Account(db.Model):  # 用户账户,用户名密码之类的
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'account'

    uid = db.Column(db.String(36), primary_key=True,
                    default=lambda: str(uuid.uuid4()))  # 用uuid应该是为了防止用户名冲突
    passwd = db.Column(db.String(100), default="")
    permission = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    credentials = db.relationship("Credential", back_populates="account")
    user_info = db.relationship("UserInfo",
                                back_populates="account", uselist=False)
    mytimetable = db.relationship("MyTimetable", back_populates="account")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.uid)


class Credential(db.Model):
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'credential'
    __table_args__ = (
            db.PrimaryKeyConstraint('cred_type', 'cred_value'),
        )

    cred_type = db.Column(db.Enum("email", "phone", "name"))
    cred_value = db.Column(db.String(64), unique=True)
    uid = db.Column(db.String(36), db.ForeignKey(Account.uid))

    account = db.relationship(Account,
                              back_populates="credentials", uselist=False)


class UserInfo(db.Model):  # 用户信息,学号部门之类的
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'user_info'

    uid = db.Column(db.String(36), db.ForeignKey(Account.uid), primary_key=True)
    student_id = db.Column(db.Integer, unique=True)
    grade = db.Column(db.String(64))
    department = db.Column(db.String(128))
    school = db.Column(db.String(128))
    major = db.Column(db.String(128))
    qq = db.Column(db.String(64), unique=True)
    introduction = db.Column(db.Text)

    account = db.relationship(Account,
                              back_populates="user_info", uselist=False)


class Applications(db.Model):
    __talbename__ = current_app.config["TABLE_PREFIX"] + 'application'

    id = db.Column(db.Integer)
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    grade = db.Column(db.String(64))
    school = db.Column(db.String(128))
    major = db.Column(db.String(128))
    phone = db.Column(db.String(64), unique=True)
    qq = db.Column(db.String(64), unique=True)
    department = db.Column(db.String(128))
    introduction = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    admission = db.Column(db.Boolean, default=False)


class ApplyTime(db.Model):
    __talbename__ = current_app.config["TABLE_PREFIX"] + 'apply_time'

    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(64), default='')
    end = db.Column(db.String(64), default='')


class Timetable(db.Model):
    __talbename__ = current_app.config["TABLE_PREFIX"] + 'timetable'

    cls = db.Column(db.Integer, primary_key=True)
    mon = db.Column(db.Integer, default=0)
    tue = db.Column(db.Integer, default=0)
    wed = db.Column(db.Integer, default=0)
    thur = db.Column(db.Integer, default=0)
    fri = db.Column(db.Integer, default=0)
    sat = db.Column(db.Integer, default=0)
    sun = db.Column(db.Integer, default=0)


class MyTimetable(db.Model):
    __talbename__ = current_app.config["TABLE_PREFIX"] + 'my_timetable'

    cls = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), db.ForeignKey(Account.uid))
    mon = db.Column(db.Integer, default=0)
    tue = db.Column(db.Integer, default=0)
    wed = db.Column(db.Integer, default=0)
    thur = db.Column(db.Integer, default=0)
    fri = db.Column(db.Integer, default=0)
    sat = db.Column(db.Integer, default=0)
    sun = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    account = db.relationship(Account,
                              back_populates="mytimetable", uselist=False)


class Notification(db.Model):
    __talbename__ = current_app.config["TABLE_PREFIX"] + 'notification'

    title = db.Column(db.String(128), primary_key=True)
    department = db.Column(db.String(128))
    content = db.Column(db.Text)
    cred_at = db.Column(db.DateTime, default=datetime.datetime.now)

    noti_member = db.relationship('NotiMember', back_populates='notifications')


class NotiMember(db.Model):
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'noti_members'
    __table_args__ = (
            db.PrimaryKeyConstraint('title', 'uid'),
        )

    title = db.Column(db.String(128), db.ForeignKey(Notification.title))
    uid = db.Column(db.String(36))
    name = db.Column(db.String(64))
    cred_at = db.Column(db.DateTime, default=datetime.datetime.now)

    notifications = db.relationship(Notification, back_populates="noti_member")


class Mission(db.Model):
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'mission'

    id = db.Column(db.Integer, primary_key=True)
    act_name = db.Column(db.String(64))
    act_date = db.Column(db.String(64))
    cred_at = db.Column(db.DateTime, default=datetime.datetime.now)
    end = db.Column(db.Boolean, default=False)

    mn_member = db.relationship("MnMember", back_populates="missions")


class MnMember(db.Model):
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'mn_members'
    __table_args__ = (
            db.PrimaryKeyConstraint('id', 'uid'),
        )

    id = db.Column(db.Integer, db.ForeignKey(Mission.id))
    uid = db.Column(db.String(36))
    name = db.Column(db.String(64))
    act_content = db.Column(db.Text)
    remarks = db.Column(db.Text)

    missions = db.relationship(Mission, back_populates="mn_member")

