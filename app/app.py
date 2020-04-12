import os

from flask import Flask
from flask_restful import Resource, Api
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("config_base")
app.config.from_envvar("APPLICATION_SETTINGS")


api = Api(app)


class Home(Resource):
    def get(self):
        return {"message": "Hello."}


api.add_resource(Home, "/")

if __name__ == "__main__":
    app.run(port=os.environ.get("PORT"))
