import os
import sys

from flask import Flask
import fire
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)
path = os.environ.get("PASSENGER_BASE_PATH")
sys.path.append(path)

from extension import db, ma  # noqa: F402


# ======================
# create app
# ======================


def create_app():
    config_str = "config.DevelopmentConfig"

    app = Flask("console")
    app.config.from_object(config_str)
    db.init_app(app)
    ma.init_app(app)

    return app


app = create_app()
app.app_context().push()


# ======================
# scripts
# ======================


class Update_Database_Records(object):
    def set_dataset_to_lims(self):
        tables = [
            "cores",
            "expeditions",
            "holes",
            "samples",
            "samples_taxa",
            "sections",
            "sites",
        ]
        for table in tables:
            print(table)
            db.engine.execute(
                f"UPDATE {table} set dataset = 'LIMS' where dataset IS NULL;"
            )


if __name__ == "__main__":
    fire.Fire(Update_Database_Records)
