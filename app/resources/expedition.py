from flask_restful import Resource


class ExpeditionListResource(Resource):
    def get(self):
        return {"data": "expeditions"}
