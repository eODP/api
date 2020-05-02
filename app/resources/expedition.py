from flask_restful import Resource

from schemas.expedition import ExpeditionSchema
from models.expedition import ExpeditionModel

expedition_list_schema = ExpeditionSchema(many=True)


class ExpeditionListResource(Resource):
    def get(self):
        return {"data": expedition_list_schema.dump(ExpeditionModel.find_all())}
