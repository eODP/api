from http import HTTPStatus

from flask_restful import Resource
from flask import request

from schemas.expedition import ExpeditionSchema
from models.expedition import Expedition

expedition_schema = ExpeditionSchema()
expedition_list_schema = ExpeditionSchema(many=True)


class ExpeditionListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)

        return expedition_list_schema.dump(Expedition.find_all(page)), HTTPStatus.OK


class ExpeditionResource(Resource):
    def get(self, id):
        expedition = Expedition.find_by_id(id)
        if expedition:
            return expedition_schema.dump(expedition), HTTPStatus.OK
        else:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND
