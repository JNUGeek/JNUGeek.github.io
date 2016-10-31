# DO NOT IMPORT FLASK BASED LIBRARIES IN THIS FILE

from datetime import timedelta
import os


class ApiConfig:
    APPNAME = "assoplat"
    TABLE_PREFIX = "geek_"
    SECRET_KEY = "Too Young Too Simple, Sometimes Naive"

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN = 'chengtianyang523@sina.com'

    # administrator list
    ADMINS = ['chengtiyanyang@gmail.com']


class ApiDebugConfig(ApiConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql://root:passwd@localhost/cty'
    SQLALCHEMY_ECHO = True


class ApiTestConfig(ApiDebugConfig):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # memory database
    SQLALCHEMY_ECHO = True


config = ApiDebugConfig()

