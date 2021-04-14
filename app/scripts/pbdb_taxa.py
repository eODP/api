import requests
import os
import csv
import sys

from flask import Flask
import fire
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)
if os.environ.get("ENV") == "Production":
    path = os.environ.get("PASSENGER_BASE_PATH")
    sys.path.append(path)

from extension import db, ma  # noqa: F402
from models.taxon import Taxon  # noqa: F402
from scripts.utils.pbdb_utils import format_taxon_name  # noqa: F402

# NOTE: must import multiple unused models to make model relationships work
from models.core import Core  # noqa: F401
from models.expedition import Expedition  # noqa: F401
from models.hole import Hole  # noqa: F401
from models.sample import Sample  # noqa: F401
from models.section import Section  # noqa: F401
from models.site import Site  # noqa: F401
from models.sample_taxon import SampleTaxon  # noqa: F401


PBDB_API = "https://paleobiodb.org/data1.2/"
PBDB_TAXA = f"{PBDB_API}taxa/single.json?vocab=pbdb&name="
LOG = "./app/scripts/tmp/pbdb_taxa_errors.csv"


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
# lookup pbdb
# ======================


def handle_not_found_error(response, taxon_name):
    data = response.json()
    if not os.path.isfile(LOG):
        with open(LOG, "w") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["taxa", "status_code", "errors", "warnings"])

    with open(LOG, "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        fields = [
            taxon_name,
            data["status_code"],
            data["errors"][0],
            data["warnings"][0],
        ]
        csvwriter.writerow(fields)


def handle_multiple_taxa_found(taxon_name):
    with open(LOG, "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        fields = [
            taxon_name,
            200,
            f'multiple taxa match "{taxon_name}"',
        ]
        csvwriter.writerow(fields)


def add_pbdb_data(taxon, keyword, notes):
    response = requests.get(f"{PBDB_TAXA}{keyword}")

    if response.status_code == 200:
        data = response.json()["records"]
        if len(data) == 1:
            taxon.pbdb_data = data[0]
            taxon.pbdb_taxon_id = data[0]["taxon_no"]
            taxon.pbdb_taxon_name = data[0]["taxon_name"]
            taxon.pbdb_taxon_rank = data[0]["taxon_rank"]
            taxon.pbdb_notes = notes
            db.session.commit()
        else:
            handle_multiple_taxa_found(taxon.name)
    else:
        handle_not_found_error(response, taxon.name)


# ======================
# scripts
# ======================


class PBDB_Taxa(object):
    def exact_taxon_match(self):
        taxon_group = "nannofossils"
        taxa = Taxon.query.filter_by(taxon_group=taxon_group, pbdb_taxon_id=None)

        for taxon in taxa:
            name = format_taxon_name(taxon)
            add_pbdb_data(taxon, name, "exact taxon match")
            print(taxon.name, ":", name)

    def genus_match(self):
        taxon_group = "nannofossils"
        taxa = Taxon.query.filter_by(taxon_group=taxon_group, pbdb_taxon_id=None)

        for taxon in taxa:
            if taxon.genus_name:
                name = taxon.genus_name
                add_pbdb_data(taxon, name, "genus match")
                print(taxon.name, ":", name)


if __name__ == "__main__":
    fire.Fire(PBDB_Taxa)
