from http import HTTPStatus

from flask_restful import Resource
from flask import request

from schemas.hole import HoleSchema
from models.hole import Hole

hole_schema = HoleSchema()
hole_list_schema = HoleSchema(many=True)


class HoleListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)

        return hole_list_schema.dump(Hole.find_all(page)), HTTPStatus.OK


class HoleResource(Resource):
    def get(self, id):
        hole = Hole.find_by_id(id)
        if hole:
            return hole_schema.dump(hole), HTTPStatus.OK
        else:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND
