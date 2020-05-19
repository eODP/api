from http import HTTPStatus

from flask_restful import Resource
from flask import request

from schemas.site import SiteSchema
from models.site import Site

site_schema = SiteSchema()
site_list_schema = SiteSchema(many=True)


class SiteListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)

        return site_list_schema.dump(Site.find_all(page)), HTTPStatus.OK


class SiteResource(Resource):
    def get(self, id):
        site = Site.find_by_id(id)
        if site:
            return site_schema.dump(site), HTTPStatus.OK
        else:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND
