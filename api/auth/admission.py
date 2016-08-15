# -*- coding: utf-8 -*-

"""游客查询录取"""


import flask_restful as restful
from flask_restful import reqparse

import common.models as models
from common.error import (
        AdmissionInfoNotFound
    )


class Admission(restful.Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('student_id', type=int)

        args = parser.parse_args()

        admission_info = models.Applications.query.get(args['student_id'])
        if not admission_info:
            raise AdmissionInfoNotFound("This student id hasn't provided any information")

        if admission_info.admission is False:
            return False

        return True

Entry = Admission
