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

    def import_samples_fields(self):
        fields_df = pd.read_csv(FIELDS_PATH)
        original_new_dict = {
            row["original_name"]: row["name"] for idx, row in fields_df.iterrows()
        }
        original_fields = set(original_new_dict.keys())

        for path in MICROPAL_CSVS:
            print(path)
            df = pd.read_csv(path, dtype=str)
            df.dropna(how="all", axis=1, inplace=True)
            df.dropna(how="all", axis=0, inplace=True)

            columns = [col.strip() for col in df.columns]
            nontaxa_fields = set(columns).intersection(original_fields)

            fields_dict = {
                field: {"name": original_new_dict[field]} for field in nontaxa_fields
            }

            relative_path = path.split("cleaned_data/")[-1]
            field_ids = fetch_field_ids(fields_dict)

            for index, row in df.iterrows():
                if row["Exp"] == "" or pd.isna(row["Exp"]):
                    continue

                sample = find_sample_by_eodp_id({"eodp_id": row["eodp_id"]})
                if sample:
                    for field_name in nontaxa_fields:
                        if pd.isna(row[field_name]):
                            continue

                        data = {
                            "sample_id": sample.id,
                            "field_id": field_ids[field_name]["field_id"],
                            "value": row[field_name],
                        }
                        sample_field = find_sample_field_by_ids(data)

                        if sample_field is None:
                            attrs = {
                                "sample_id": sample.id,
                                "field_id": field_ids[field_name]["field_id"],
                                "value": row[field_name],
                                "data_source_notes": relative_path,
                                "original_name": field_name

                            }
                            create_sample_field(attrs)
                else:
                    raise ValueError(f"Invalid sample {row['Sample']} {row['Exp']}")


if __name__ == "__main__":
    fire.Fire(Import_Normalized_Fields)
