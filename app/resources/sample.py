from http import HTTPStatus

from flask_restful import Resource
from flask import request

from schemas.sample import SampleSchema
from models.sample import Sample

sample_schema = SampleSchema()
sample_list_schema = SampleSchema(many=True)


class SampleListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        data_source_type = request.args.get("data_source_type", "", type=str)

        return (
            sample_list_schema.dump(Sample.find_all(page, data_source_type)),
            HTTPStatus.OK,
        )


class SampleResource(Resource):
    def get(self, id):
        sample = Sample.find_by_id(id)
        if sample:
            return sample_schema.dump(sample), HTTPStatus.OK
        else:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND
