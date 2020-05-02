from flask_restful import Resource
from flask import request

from schemas.expedition import ExpeditionSchema
from models.expedition import ExpeditionModel

expedition_list_schema = ExpeditionSchema(many=True)


class ExpeditionListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)

        return {"data": expedition_list_schema.dump(ExpeditionModel.find_all(page))}
