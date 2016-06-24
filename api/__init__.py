def get_blueprint():
    from flask_restful import Api
    from flask import Blueprint

    from common.utils import find_modules, join_url

    bp = Blueprint('api', __name__)
    api = Api(bp)

    for modname in find_modules(__file__):
        mod = __import__(modname, globals=globals(), locals=locals(), level=1)
        if hasattr(mod, "get_entries"):
            for entname, entry in mod.get_entries():
                api.add_resource(entry, join_url(modname, entname),
                        endpoint="{}.{}".format(modname, entname))

    return bp

