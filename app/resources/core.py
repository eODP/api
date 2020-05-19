from http import HTTPStatus

from flask_restful import Resource
from flask import request

from schemas.core import CoreSchema
from models.core import Core

core_schema = CoreSchema()
core_list_schema = CoreSchema(many=True)


class CoreListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)

        return core_list_schema.dump(Core.find_all(page)), HTTPStatus.OK


class CoreResource(Resource):
    def get(self, id):
        core = Core.find_by_id(id)
        if core:
            return core_schema.dump(core), HTTPStatus.OK
        else:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND
