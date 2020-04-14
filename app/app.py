import os

from flask import Flask
from flask_restful import Resource, Api
from dotenv import load_dotenv


load_dotenv(".env", verbose=True)

if os.environ.get("ENV") == "Production":
    config_str = "api.app.config.ProductionConfig"
else:
    config_str = "config.DevelopmentConfig"

app = Flask(__name__)
app.config.from_object(config_str)

api = Api(app)


class Home(Resource):
    def get(self):
        return {"message": "Hello."}


api.add_resource(Home, "/")

if __name__ == "__main__":
    app.run(port=os.environ.get("PORT"))
