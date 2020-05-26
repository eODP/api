from http import HTTPStatus

from flask_restful import Resource


class ApiHomeResource(Resource):
    def get(self):
        description = {
            "description": "eODP REST API guide",
            "routes": [
                {
                    "description": "Summary of available endpoints",
                    "methods": "GET",
                    "url": "/api",
                },
                {
                    "description": "Returns all cores",
                    "methods": "GET",
                    "url": "/api/cores",
                },
                {
                    "description": "Returns one core",
                    "methods": "GET",
                    "url": "/api/cores/<id>",
                },
                {
                    "description": "Returns all expeditions",
                    "methods": "GET",
                    "url": "/api/expeditions",
                },
                {
                    "description": "Returns one expedition",
                    "methods": "GET",
                    "url": "/api/expeditions/<id>",
                },
                {
                    "description": "Returns all holes",
                    "methods": "GET",
                    "url": "/api/holes",
                },
                {
                    "description": "Returns one hole",
                    "methods": "GET",
                    "url": "/api/holes/<id>",
                },
                {
                    "description": "Returns all samples",
                    "methods": "GET",
                    "url": "/api/samples",
                },
                {
                    "description": "Returns one sample",
                    "methods": "GET",
                    "url": "/api/samples/<id>",
                },
                {
                    "description": "Returns all sections",
                    "methods": "GET",
                    "url": "/api/sections",
                },
                {
                    "description": "Returns one section",
                    "methods": "GET",
                    "url": "/api/sections/<id>",
                },
                {
                    "description": "Returns all sites",
                    "methods": "GET",
                    "url": "/api/sites",
                },
                {
                    "description": "Returns one site",
                    "methods": "GET",
                    "url": "/api/sites/<id>",
                },
            ],
            "v": 0.1,
        }

        return description, HTTPStatus.OK
