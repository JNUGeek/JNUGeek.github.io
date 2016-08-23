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

        admission_info = models.Applications.query.filter_by(student_id=args['student_id']).first()
        if not admission_info:
            raise AdmissionInfoNotFound("This student id hasn't applied")

        admission = admission_info.admission
        if admission is False:
            return {admission: False}

        return {admission: True}

Entry = Admission
