import unittest
import werkzeug
import hashlib
import json

from flask import current_app, url_for, session

from common.models import (
        Account,
        Credential,
        UserInfo,
        MyTimetable,
        Applications
    )
from common.error import *
from common.utils import ApiTest, test_context


class AuthTest(ApiTest):

    def setUp(self):
        super(AuthTest, self).setUp()

        self.account_1 = Account(
                passwd=hashlib.md5(b"123pass").hexdigest()
            )
        self.account_2 = Account()

        self.dbsess.add(self.account_1)
        self.dbsess.add(self.account_2)
        self.dbsess.flush()
        self.dbsess.add(Credential(
                uid=self.account_1.uid,
                cred_type='name',
                cred_value='john'
            ))
        self.dbsess.add(MyTimetable(
                uid=self.account_1.uid
        ))
        self.dbsess.add(MyTimetable(
                uid=self.account_2.uid
        ))
        self.dbsess.add(Credential(
                uid=self.account_2.uid,
                cred_type='name',
                cred_value='gump'
            ))
        self.dbsess.add(Credential(
                uid=self.account_2.uid,
                cred_type='email',
                cred_value='gump@gump.com'
            ))
        self.dbsess.add(UserInfo(
                uid=self.account_2.uid,
                student_id=2013999999,
                department=u'\u4e00\u70b9\u4eba\u751f\u7684\u7ecf\u9a8c',
                school=u'\u4e00\u70b9\u5fae\u5c0f\u7684\u5de5\u4f5c',
                introduction=u'\u4e00\u4e2a\u4e0a\u6d77\u7684\u4e66\u8bb0'
            ))
        self.dbsess.add(Applications(
                name='paul',
                student_id=2015000000,
                school='ist',
                major='cst',
                phone='15500000000',
                department='技术组'
        ))
        self.dbsess.add(Applications(
                name='ann',
                student_id=2015000001,
                school='ist',
                major='cst',
                phone='15500000001',
                department='技术组'
        ))
        self.dbsess.commit()

    @test_context
    def test_create_account(self):
        response = self.post(
                endpoint="api.auth.account",
                data={'name': 'bill'}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertRegexpMatches(data["uid"], "[0-9a-z\-]{36}")

    @test_context
    def test_create_duplicated_account(self):
        response = self.post(
                endpoint="api.auth.account",
                data={'name': 'john'}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertApiError(data, AccountAlreadyExists)

    @test_context
    def test_application(self):
        response = self.post(
                endpoint="api.guest.application",
                data={'name': 'paul',
                      'student_id': 2015000000,
                      'school': 'ist',
                      'major': 'cst',
                      'phone': '15500000000',
                      'department': '技术组'}
            )
        data = self.load_data(response.data)
        self.assertEqual(response.status_code, 200)

    @test_context
    def test_admission(self):
        response = self.get(
                endpoint="api.guest.admission",
                data={
                      'student_id': 2015000000
                      }
            )
        data = self.load_data(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['admission'], False)

    @test_context
    def test_contact(self):
        self.login_user(self.account_1)
        response = self.get(
                endpoint="api.auth.contact",
                data={'name': 'gump'}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['school'], self.account_2.user_info.school)
        self.assertEqual(data['student_id'], self.account_2.user_info.student_id)

    @test_context
    def test_contact_not_exists(self):
        self.login_user(self.account_1)
        response = self.get(
                endpoint="api.auth.contact",
                data={'name': 'peter'}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertApiError(data, UserInfoNotFound)

    @test_context
    def test_timetable(self):
        self.login_user(self.account_1)
        response = self.post(
                endpoint="api.auth.timetable",
                data={'timetable': [1, 1, 1, 1, 1, 1, 1,
                                    0, 0, 0, 0, 0, 0, 0,
                                    1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1]
                      }
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_get_timetable(self):
        self.login_user(self.account_1)
        response = self.get(
                endpoint="api.auth.timetable",
                data={}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_successful_login_no_password(self):
        response = self.post(
                endpoint="api.auth.login",
                data={'name': 'gump'}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertRegexpMatches(data["uid"], "[0-9a-z\-]{36}")
        self.assertEqual(session["user_id"], self.account_2.uid)

    @test_context
    def test_successful_login_with_password(self):
        response = self.post(
                endpoint="api.auth.login",
                data={
                    'name': 'john',
                    'passwd': hashlib.md5(b"123pass").hexdigest()
                }
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertRegexpMatches(data["uid"], "[0-9a-z\-]{36}")
        self.assertEqual(session["user_id"], self.account_1.uid)

    @test_context
    def test_login_password_incorrect(self):
        response = self.post(
                endpoint="api.auth.login",
                data={
                    'name': 'john',
                    'passwd': hashlib.md5(b"wrong").hexdigest(),
                }
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertApiError(data, PasswordIncorrect)

    @test_context
    def test_logout_without_having_logged_in(self):
        response = self.post(
                endpoint="api.auth.logout",
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 401)

    @test_context
    def test_logout_user(self):
        self.login_user(self.account_1)
        self.assertEqual(session["user_id"], self.account_1.uid)

        response = self.post(
                endpoint="api.auth.logout",
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['uid'], self.account_1.uid)
        self.assertNotIn("user_id", session)

    @test_context
    def test_user_info_add_new(self):
        self.login_user(self.account_1)
        response = self.post(
                endpoint="api.auth.userinfo",
                data={
                    'student_id': 114514,
                    'department': 'Computer Science',
                }
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['uid'], self.account_1.uid)

        self.assertEqual(self.account_1.user_info.department,
                         'Computer Science')

    @test_context
    def test_user_info_query_self(self):
        self.login_user(self.account_2)
        response = self.get(
                endpoint="api.auth.userinfo",
                data={
                    'info': ['introduction', 'school'],
                }
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['school'], self.account_2.user_info.school)

    @test_context
    def test_user_info_query_others(self):
        response = self.get(
                endpoint="api.auth.userinfo",
                data={
                    'uid': self.account_2.uid,
                    'info': ['introduction', 'school'],
                }
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['school'], self.account_2.user_info.school)

    @test_context
    def test_see_applications(self):
        response = self.get(
                endpoint="api.admin.application",
                data={}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['1']['name'], 'paul')

    @test_context
    def test_prove_applications(self):
        response = self.post(
                endpoint="api.admin.application",
                data={'name': ['paul', 'ban'],
                      'student_id': [2015000000, 2015000002],
                      'school': ['ist', 'aaa'],
                      'major': ['cst', 'bbb'],
                      'phone': ['15500000000', '15500000003'],
                      'department': ['技术组', '媒宣组']
                      }
            )
        data = self.load_data(response.data)
        print(data)

        self.assertEqual(response.status_code, 200)


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(AuthTest))

