# DO NOT IMPORT FLASK BASED LIBRARIES IN THIS FILE

from datetime import timedelta


class ApiConfig:
    APPNAME = "JNUHeek2015"
    TABLE_PREFIX = "geek_"
    SECRET_KEY = "Try to make big news."

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ApiDebugConfig(ApiConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql://root:ctyyx@localhost/cty'
    SQLALCHEMY_ECHO = True


class ApiTestConfig(ApiDebugConfig):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # memory database
    SQLALCHEMY_ECHO = True


config = ApiDebugConfig()

