# -*- coding: utf-8 -*-

"""评价课程"""


import flask_restful as restful
from flask_restful import reqparse
from flask import g
import common.models as models
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from common.error import *


class CourseEvaluation(restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('course_name', type=str, required=True)
        parser.add_argument('course_type', type=str, required=True)
        parser.add_argument('teacher', type=str, required=True)
        parser.add_argument('evaluation', type=str, required=True)

        args = parser.parse_args()

        new_evaluation = models.CouresEvaluate()
        for info in args.keys():
            if not args[info]:
                continue
            setattr(new_evaluation, info, args[info])
        g.db.session.add(new_evaluation)
        try:
            g.db.session.commit()
        except IntegrityError:
            raise EvaluationAlreadyExists()
        except OperationalError:
            raise InformationCannotBeNull

        return {'id': new_evaluation.id}

Entry = CourseEvaluation
