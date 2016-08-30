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
        Applications,
        ApplyTime,
        Mission,
        MnMember,
        Timetable,
        Notification
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
        self.account_3 = Account(
                passwd=hashlib.md5(b"123").hexdigest()
            )

        self.dbsess.add(self.account_1)
        self.dbsess.add(self.account_2)
        self.dbsess.add(self.account_3)
        self.dbsess.flush()
        self.dbsess.add(Credential(
                uid=self.account_1.uid,
                cred_type='name',
                cred_value='john'
            ))
        self.dbsess.add(Credential(
                uid=self.account_3.uid,
                cred_type='name',
                cred_value='patrick'
            ))
        self.dbsess.add(MyTimetable(
                uid=self.account_1.uid,
                mon=1,
                wed=1
        ))
        self.dbsess.add(MyTimetable(
                uid=self.account_1.uid,
                sat=1
        ))
        self.dbsess.add(MyTimetable(
                uid=self.account_2.uid,
                tue=1
        ))
        self.dbsess.add(MyTimetable(
                uid=self.account_3.uid,
                sun=1
        ))
        self.dbsess.add(Timetable(
                mon=1,
                wed=1
        ))
        self.dbsess.add(Timetable(
                sat=1
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
        self.dbsess.add(UserInfo(
                uid=self.account_3.uid,
                student_id=2013,
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
        self.dbsess.add(ApplyTime(
            start='9.12',
            end='10.12'
        ))
        self.dbsess.add(Mission(
            id=1,
            act_name='night',
            act_date='5.23',
        ))
        self.dbsess.add(MnMember(
            id=1,
            uid=self.account_1.uid,
            name='john',
            act_content='this'
        ))
        self.dbsess.add(MnMember(
            id=1,
            uid=self.account_2.uid,
            name='gump',
            act_content='that'
        ))
        self.dbsess.add(Notification(
            title='a title',
            department='技术组',
            content='get girls'
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

    @test_context
    def test_change_appliytime(self):
        response = self.post(
                endpoint="api.admin.applytime",
                data={'start': '9.12',
                      'end': '10.12'}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_see_appliytime(self):
        response = self.get(
                endpoint="api.admin.applytime",
                data={}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['start'], '9.12')

    @test_context
    def test_post_mission(self):
        response = self.post(
                endpoint="api.admin.mission",
                data={'act_name': 'newcomer\'s night',
                      'act_date': '9.12',
                      'name': ['gump', 'john'],
                      'act_content': ['eat', 'sleep'],
                      'remarks': ['', '']}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_see_mission(self):
        self.login_user(self.account_2)
        response = self.get(
                endpoint="api.admin.mission",
                data={}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['last'][0], 'night')

    @test_context
    def test_see_fullmission(self):  # 这里有问题,明天再来
        self.login_user(self.account_2)
        response = self.get(
                endpoint="api.admin.fullmission",
                data={'id': 1}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_see_fullmission(self):
        self.login_user(self.account_2)
        response = self.get(
                endpoint="api.auth.get_mission",
                data={}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_member_see_fullmn(self):
        self.login_user(self.account_2)
        response = self.get(
                endpoint="api.auth.get_fullmn",
                data={'id': 1}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_add_member(self):
        response = self.post(
                endpoint="api.admin.member",
                data={'name': 'peter',
                      'student_id': '2015000004',
                      'grade': '大一',
                      'school': 'ist',
                      'major': 'se',
                      'phone': '15500000002',
                      }
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_see_members(self):
        response = self.get(
                endpoint="api.admin.member",
                data={}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_delete_members(self):
        response = self.get(
                endpoint="api.admin.deletemember",
                data={'student_id': 2013}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_see_timetable(self):
        response = self.get(
                endpoint="api.admin.timetable",
                data={'user': 'john'}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_see_general_timetable(self):
        response = self.get(
                endpoint="api.admin.timetable",
                data={}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_notify_with_specific_member(self):
        response = self.post(
                endpoint="api.admin.notify",
                data={'title': 'party',
                      'department': '其他',
                      'members': ['john', 'gump'],
                      'content': 'have fun'
                      }
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_notify_with_department(self):
        response = self.post(
                endpoint="api.admin.notify",
                data={'title': 'party',
                      'department': '技术组',
                      'content': 'have fun'
                      }
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_see_notification(self):
        response = self.get(
                endpoint="api.admin.notify",
                data={}
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)

    @test_context
    def test_member_see_fullmn(self):
        self.login_user(self.account_2)
        response = self.get(
                endpoint="api.auth.get_notification"
            )
        data = self.load_data(response.data)

        self.assertEqual(response.status_code, 200)


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(AuthTest))

