"""将这个目录下的所有入口收集起来注册到蓝图上"""


def get_blueprint():
    from flask_restful import Api
    from flask import Blueprint

    from common.utils import find_modules, join_url

    # 注册了蓝图并初始化应用
    bp = Blueprint('api', __name__)
    api = Api(bp)

    for modname in find_modules(__file__):
        mod = __import__(modname, globals=globals(), locals=locals(), level=1)
        if hasattr(mod, "get_entries"):
            for entname, entry in mod.get_entries():  # 主要是这里面一个个的add很麻烦
                api.add_resource(entry, join_url(modname, entname),
                        endpoint="{}.{}".format(modname, entname))

    return bp

