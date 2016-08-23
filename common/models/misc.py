"""杂项"""

from flask import g, current_app

db = g.db

import datetime
import uuid


class Session(db.Model):
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'session'

    sid = db.Column(db.String(36), primary_key=True,
                    default=lambda: str(uuid.uuid4()))
    data = db.Column(db.LargeBinary)  # 二进制
    expiry = db.Column(db.DateTime)

