from flask_restful import Resource
from flask import request

from schemas.site import SiteSchema
from models.site import SiteModel

site_list_schema = SiteSchema(many=True)


class SiteListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)

        return {"data": site_list_schema.dump(SiteModel.find_all(page))}
