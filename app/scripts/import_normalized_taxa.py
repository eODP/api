import os
import csv
import glob
import sys

from flask import Flask
import fire
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)
if os.environ.get("ENV") == "Production":
    path = os.environ.get("PASSENGER_BASE_PATH")
    sys.path.append(path)

from extension import db, ma  # noqa: F402
from scripts.utils.import_records import (  # noqa: F402
    find_taxon_by_name,
    create_taxon,
    create_taxon_crosswalk,
)

TAXON_GROUP = "nannofossils"
FILE_PATH = os.environ.get("RAW_DATA_PATH")
TAXA_CSV = f"{FILE_PATH}/taxa/taxa_list_{TAXON_GROUP}.csv"
TAXA_CROSSWALK_CSV = f"{FILE_PATH}/taxa/taxa_crosswalk_{TAXON_GROUP}.csv"

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


class Import_Normalized_Taxa(object):
    def clear_table(self, table):
        db.engine.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE;")

    def import_taxa(self):
        with open(TAXA_CSV, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                create_taxon({"name": row["name"], "taxon_group": row["taxon_group"]})

    def import_taxa_crosswalk(self):
        with open(TAXA_CROSSWALK_CSV, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                taxon = find_taxon_by_name(
                    {"name": row["final_name"], "taxon_group": row["taxon_group"]}
                )

                create_taxon_crosswalk(
                    {
                        "taxon_id": taxon.id,
                        "taxon_group": row["taxon_group"],
                        "original_name": row["name"],
                    }
                )


if __name__ == "__main__":
    fire.Fire(Import_Normalized_Taxa)
