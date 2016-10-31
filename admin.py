#!/usr/bin/env python3

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

# if sys.version_info > (2, 7):
#    warnings.warn("Due to few flask extensions having supported Py3k, "
#            "please check carefully if your code is fully compatible.")

# prepend project root path to module search paths

import inspect
from flask import g, current_app

registered_command = {}


def as_command(arg=""):

    def reg(func):
        global registered_command
        true_name = arg
        if arg is "":
            true_name = func.__name__
        registered_command[true_name] = func
        return func

    return reg

################################################################################
# Commands

_RECORD_STR = u"""
### {method} {url}

Input Data:

> {user} is logged in.

```
{indata}
```

Output Data:

```
{outdata}
```
"""


@as_command()
def run(port=5000):
    current_app.run(port=port, debug=True)


@as_command()
def test(dbecho=False, record=""):
    global _RECORD_STR

    import unittest
    import common.config
    import api.auth.tests

    current_app.config.from_object(common.config.ApiTestConfig)
    current_app.config["SQLALCHEMY_ECHO"] = dbecho

    unittest.TextTestRunner().run(api.auth.tests.suite)

    if record:
        from common.utils import whole_record
        record_file = open(record, "w")
        record_file.write("# API List\n\n[TOC]\n\n")
        for title, contents in sorted(whole_record.items()):
            record_file.write("## %s\n\n" % title)
            for section in contents:
                if isinstance(section, str):
                    record_file.write(section + '\n')
                elif isinstance(section, dict):
                    record_file.write(_RECORD_STR.format(**section))
        record_file.close()


@as_command()
def initdb(drop=False):
    if not drop:
        g.db.create_all()
    else:
        g.db.drop_all()


@as_command()
def help(func=None):
    global registered_command

    if func is None:
        print("Available commands:")
        for ln in registered_command.keys():
            print("    " + ln)
    else:
        if func in registered_command:
            print("Arguments of %s:" % func)
            ca = inspect.getcallargs(registered_command[func])
            for k, d in ca.items():
                print("    --%s\t\t(default: %s)" % (k, repr(d)))

################################################################################


def parse_arguments(arg_list):
    args = []
    kwargs = {}

    setting_key = None

    for a in arg_list:
        if setting_key and a[:2] == "--":
            kwargs[setting_key] = True
            setting_key = None

        if setting_key is None:
            if a[:2] == "--":
                setting_key = a[2:]
            else: args += [a]
        else:
            kwargs[setting_key] = a
            setting_key = None

    if setting_key:
        kwargs[setting_key] = True
        setting_key = None

    return args, kwargs


def run_command():
    if len(sys.argv) == 1:
        sys.argv += ['help']

    if sys.argv[1] in registered_command:
        func = registered_command[sys.argv[1]]
        args, kwargs = parse_arguments(sys.argv[2:])
        func(*args, **kwargs)
    else:
        print("No such command. Run ./admin.py help for more information.")
        exit(255)



import common.init

app = common.init.get_app()
    
with app.app_context():
    common.init.init_everything()
    run_command()




