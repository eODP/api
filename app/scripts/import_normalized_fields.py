import os
import glob
import sys
import pandas as pd

from flask import Flask
import fire
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)
path = os.environ.get("PASSENGER_BASE_PATH")
sys.path.append(path)

from extension import db, ma  # noqa: F402
from scripts.utils.import_records import (  # noqa: F402
    find_field_by_name,
    create_field,
    fetch_field_ids,
    find_sample_by_eodp_id,
    find_sample_field_by_ids,
    create_sample_field,
)


FILE_PATH = os.environ.get("CLEANED_DATA_PATH")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH")
PI_FILES_PATH = os.environ.get("PI_FILES_PATH")

MICROPAL_CSVS = glob.glob(f"{FILE_PATH}/LIMS/Micropal_CSV_1/*.csv")
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/LIMS/Micropal_CSV_2/*.csv"))
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/LIMS/Micropal_CSV_3/*.csv"))
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/LIMS/Micropal_CSV_4/*.csv"))
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/LIMS/Micropal_CSV_revised/*.csv"))


DATE = "2022-08-11"
FIELDS_PATH = f"{OUTPUT_PATH}/normalized_data/LIMS/nontaxa_fields_{DATE}.csv"
datasets = ["NOAA", "Janus", "LIMS"]
DATASET = datasets[2]

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


class Import_Normalized_Fields(object):
    def clear_table(self, table):
        db.engine.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE;")

    def import_fields(self):
        df = pd.read_csv(FIELDS_PATH)
        field_names = df["name"].unique()
        for field_name in field_names:
            field = find_field_by_name({"name": field_name.strip()})

            if field is None:
                data = {"name": field_name}
                create_field(data)

if __name__ == "__main__":
    fire.Fire(Import_Normalized_Fields)
