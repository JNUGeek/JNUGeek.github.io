# Initialize globally used variables
_app = None
_db = None
_login_manager = None

from flask import current_app


def get_app():
    global _app

    if not _app:
        from flask import Flask
        from .config import config

        _app = Flask(config.APPNAME)
        _app.config.from_object(config)

    return _app


def get_db():
    global _db

    if not _db:
        from flask_sqlalchemy import SQLAlchemy

        _db = SQLAlchemy(current_app)
        _db.init_app(current_app)

    return _db


def get_login_manager():
    global _login_manager

    if not _login_manager:
        from flask_login import LoginManager

        _login_manager = LoginManager()
        _login_manager.init_app(current_app)

    return _login_manager


################################################################################
# Initialization Items


def init_global_variables():
    from flask import g
    from werkzeug.local import LocalProxy

    g.db = LocalProxy(get_db)
    g.login_manager = LocalProxy(get_login_manager)


def init_session_interface():
    from .utils import DatabaseSessionInterface
    from .models import Session

    current_app.session_interface = DatabaseSessionInterface(get_db(), Session)


def init_user_loader():
    from .models import Account

    _lm = get_login_manager()

    @_lm.user_loader
    def load_user(uid):
        return get_db().session.query(Account).get(uid)


def init_app():
    # we still need those global variables during request
    import os
    import api
    import json
    import mimetypes
    import common.error
    from flask import render_template

    current_app.before_request(init_global_variables)

    @current_app.errorhandler(common.error.ApiError)
    def error_handler(error):
        return json.dumps(error.data), 400

    @current_app.route('/')
    def index():
        return render_template('home.html')

    @current_app.route('/login')
    def login_view():
        return render_template('login.html')

    @current_app.route('/presign')
    def presign_view():
        return render_template('pre-sign.html')

    # @current_app.route('/', defaults={'filename': 'home'})
    # @current_app.route('/<path:filename>')
    # def send_static_files(filename):
    #     if os.path.isfile(os.path.join('static', filename)):
    #         pass
    #     if os.path.isfile(os.path.join('static', filename + '.html')):
    #         filename += '.html'
    #     if os.path.isfile(os.path.join('static', filename, 'pre.html')):
    #         filename += "/pre.html"
    #
    #     resp = current_app.send_static_file(filename)
    #     resp.mimetype = mimetypes.guess_type(filename)[0]
    #
    #     return resp

    current_app.register_blueprint(api.get_blueprint(), url_prefix="/api")

################################################################################
# Initialize an app in this way:
#
#   app = init.get_app()
#   with app.app_context():
#       init.init_everything()


def init_everything():
    init_global_variables()

    init_app()
    init_session_interface()
    init_user_loader()


