from http import HTTPStatus

from flask_restful import Resource
from flask import request

from schemas.taxon import TaxonSchema
from models.taxon import Taxon

taxon_schema = TaxonSchema()
taxon_list_schema = TaxonSchema(many=True)


class TaxonListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)

        return taxon_list_schema.dump(Taxon.find_all(page)), HTTPStatus.OK


class TaxonResource(Resource):
    def get(self, id):
        taxon = Taxon.find_by_id(id)
        if taxon:
            return taxon_schema.dump(taxon), HTTPStatus.OK
        else:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND
