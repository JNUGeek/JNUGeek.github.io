import os
import re

from flask import Blueprint


def find_modules(init_file, fpattern = None):
    """
    List names of modules in the same directory as init_file. The function is
    usually used in __init__.py and returns value fit for __all__.
    If you need to import it, use __import__ with level 1.
    """

    import pkgutil

    fpattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$") \
            if fpattern is None else re.compile(fpattern)

    dirname = os.path.dirname(init_file)
    parmod = os.path.dirname(dirname)
    entries = [modname for _, modname, _ in pkgutil.iter_modules([dirname])]
    entries = list(filter(lambda n: fpattern.match(n), entries))

    return entries


def get_entries(init_file, glb):
    _entries = []

    for modname in find_modules(init_file):
        mod = __import__(modname, globals=glb, level=1)
        if hasattr(mod, "Entry"):
            _entries.append((modname, mod.Entry))

    return _entries


def join_url(*args, **kwargs):
    """
    Join a args with seps. example:

        >>> join_url("abc/", "/def/", "fed", "yui")
        '/abc/def/fed/yui/'
        >>> join_url("abc", "def#", "##fed", "yui", sep=('^', '#', '$'))
        '^abc#def##fed#yui$'

    """
    sep = kwargs["sep"] if "sep" in kwargs else ('/', '/', '/')

    concat_str = sep[0]
    concat_str += args[0][1:] if args[0][0] == sep[0] else args[0]

    for a in args[1:]:
        concat_str += "" if concat_str[-1] == sep[1] else sep[1]
        concat_str += a[1:] if a[0][0] == sep[1] else a

    concat_str += "" if concat_str[-1] == sep[2] else sep[2]

    return concat_str

################################################################################
# Request Argument Conversion and Validation


def email_type(email_str):
    if re.match("^[^@]+@[a-zA-Z0-9\-_\.]+$", email_str):
        return email_str
    else:
        raise ValueError("Not a Proper Email.")


def phone_type(phone_str):
    if re.match("^\d+$", phone_str):
        return phone_str
    else:
        raise ValueError("Not a Proper Phone Number.")


def md5_hashed_type(mhstr):
    if re.match("(^$)|(^[a-zA-Z0-9]{32}$)", mhstr):
        return mhstr
    else:
        raise ValueError("Not MD5 Hashed.")

################################################################################
# Session Interface

import pickle
import uuid

from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin


class DatabaseSession(CallbackDict, SessionMixin):
    @staticmethod
    def _update(self):
        self.modified = True

    def __init__(self, initial=None, sid=None, new=False):
        CallbackDict.__init__(self, initial, self._update)
        self.sid = sid if sid else self.get_session_id()
        self.new = new
        self.modified = False

    @staticmethod
    def get_session_id():
        return str(uuid.uuid4())


class DatabaseSessionInterface(SessionInterface):
    serializer = lambda s, d: pickle.dumps(d, protocol=2)
    unserializer = lambda s, d: pickle.loads(d)
    session_class = DatabaseSession

    def __init__(self, db, table):
        self.db = db
        self.session_table = table

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            return DatabaseSession(new=True)

        session_record = self.session_table.query.get(sid)
        if not session_record:
            return DatabaseSession(sid=sid, new=True)

        initial = self.unserializer(session_record.data)
        return DatabaseSession(sid=sid, initial=initial)

    def save_session(self, app, session, response):
        from flask import current_app
        from datetime import datetime

        assert isinstance(session, self.session_class)

        # cookie properties
        domain = self.get_cookie_domain(current_app)
        path = self.get_cookie_path(current_app)
        httponly = self.get_cookie_httponly(current_app)
        secure = self.get_cookie_secure(current_app)

        sid = session.sid
        data = self.serializer(dict(session))
        expiry = self.get_expiration_time(current_app, session)

        # clear the session
        self.db.session.rollback()

        session_record = self.session_table.query.get(sid)
        if session_record:
            session_record.data = data
            session_record.expiry = expiry
        else:
            session_record = self.session_table(
                    sid=sid,
                    data=data,
                    expiry=expiry
                )
            self.db.session.add(session_record)

        self.db.session.commit()

        response.set_cookie(current_app.session_cookie_name, sid,
                            expires=expiry,
                            domain=domain,
                            path=path,
                            httponly=httponly,
                            secure=secure
            )

################################################################################
# Test Base Class

import json
import unittest


def test_context(func):
    from flask import current_app

    def wrapper(self, *args, **kwargs):
        with current_app.test_request_context():
            with current_app.test_client() as client:
                self.client = client
                self.login_record = None

                func(self, *args, **kwargs)

                del self.client
                del self.login_record

    return wrapper

whole_record = {}


class ApiTest(unittest.TestCase):

    def jsonify(self, obj):
        import json
        return json.dumps(
                obj,
                ensure_ascii=False,
                indent=4
            )

    def record_requests(self, method, url, view, indata, response):
        global _RECORD_STR
        global whole_record

        outdata = self.load_data(response.data)
        user = "No user"
        if hasattr(self, 'login_record') and self.login_record:
            user = "User `%s`" % self.login_record

        if url not in whole_record:
            doc = ""
            if view and getattr(view, 'view_class', None):
                doc = view.view_class.__doc__ or ""
            whole_record[url] = [ doc ]

        whole_record[url] += [{
                'method': method,
                'url': url,
                'user': user,
                'indata': indata,
                'outdata': self.jsonify(outdata),
            }]

    def load_data(self, data):
        if isinstance(data, bytes):
            data = data.decode('utf8')
        return json.loads(data)

    def login_user(self, account):
        self.login_record = account.uid

        from flask import url_for
        response = self.client.post(
            path=url_for("api.auth.login"),
            data={'uid': account.uid, 'passwd': account.p}
        )
        self.assertEqual(response.status_code, 200)

    def open(self, method, endpoint, **kwargs):
        from flask import url_for, current_app
        kwargs['path'] = url_for(endpoint)

        resp = getattr(self.client, method)(**kwargs)
        view = None
        if endpoint in current_app.view_functions:
            view = current_app.view_functions[endpoint]
        indata = u'No argument.'
        if 'data' in kwargs:
            indata = kwargs['data']

        self.record_requests(
                method=method.upper(),
                url=kwargs['path'],
                view=view,
                indata=indata,
                response=resp
            )

        return resp

    def get(self, **kwargs):
        return self.open('get', **kwargs)

    def post(self, **kwargs):
        return self.open('post', **kwargs)

    def assertApiError(self, respdict, errcls):
        self.assertIn("status", respdict)
        self.assertIn("code", respdict["status"])
        self.assertEqual(respdict["status"]["code"], errcls.error_code)

    def setUp(self):
        from flask import g, current_app
        g.db.create_all()
        self.dbsess = g.db.create_scoped_session()

    def tearDown(self):
        from flask import g
        del self.dbsess
        g.db.drop_all()

