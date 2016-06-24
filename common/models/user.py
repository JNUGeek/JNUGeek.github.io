from flask import g, current_app

db = g.db

import uuid
import datetime

class Account(db.Model):
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'account'

    uid = db.Column(db.String(36), primary_key=True,
            default=lambda: str(uuid.uuid4()))
    passwd = db.Column(db.String(32), default="")
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    credentials = db.relationship("Credential", back_populates="account")
    user_info = db.relationship("UserInfo",
            back_populates="account", uselist=False)

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
    cred_value = db.Column(db.String(64))
    uid = db.Column(db.String(36), db.ForeignKey(Account.uid))

    account = db.relationship(Account,
            back_populates="credentials", uselist=False)

class UserInfo(db.Model):
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'user_info'

    uid = db.Column(db.String(36), db.ForeignKey(Account.uid), primary_key=True)
    student_id = db.Column(db.Integer)
    department = db.Column(db.String(128))
    school = db.Column(db.String(128))
    introduction = db.Column(db.Text)

    account = db.relationship(Account,
            back_populates="user_info", uselist=False)



