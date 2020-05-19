from http import HTTPStatus

from flask_restful import Resource
from flask import request

from schemas.section import SectionSchema
from models.section import Section

section_schema = SectionSchema()
section_list_schema = SectionSchema(many=True)


class SectionListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)

        return section_list_schema.dump(Section.find_all(page)), HTTPStatus.OK


class SectionResource(Resource):
    def get(self, id):
        section = Section.find_by_id(id)
        if section:
            return section_schema.dump(section), HTTPStatus.OK
        else:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND
