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
    import_expedition_for_csv,
    import_sites_for_csv,
    import_holes_for_csv,
    import_cores_for_csv,
    import_sections_for_csv,
    find_section,
    find_sample,
    create_sample,
)

FILE_PATH = os.environ.get("RAW_DATA_PATH")
MICROPAL_CSVS = glob.glob(f"{FILE_PATH}/Micropal_CSV_1/*.csv")
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/Micropal_CSV_2/*.csv"))
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/Micropal_CSV_3/*.csv"))

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


class Import_Micropal_CSV(object):
    def clear_table(self, table):
        db.engine.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE;")

    def import_expeditions(self):
        for path in MICROPAL_CSVS:
            filename = path.split("/")[-1]
            with open(path, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                import_expedition_for_csv(csv_reader, filename)

    def import_sites(self):
        for path in MICROPAL_CSVS:
            filename = path.split("/")[-1]
            with open(path, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                import_sites_for_csv(csv_reader, filename)

    def import_holes(self):
        for path in MICROPAL_CSVS:
            filename = path.split("/")[-1]
            with open(path, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                import_holes_for_csv(csv_reader, filename)

    def import_cores(self):
        for path in MICROPAL_CSVS:
            filename = path.split("/")[-1]
            with open(path, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                import_cores_for_csv(csv_reader, filename)

    def import_sections(self):
        for path in MICROPAL_CSVS:
            filename = path.split("/")[-1]
            print(filename)

            with open(path, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                import_sections_for_csv(csv_reader, filename)

    def import_samples(self):
        for path in MICROPAL_CSVS:
            filename = path.split("/")[-1]
            print(filename)

            # add encoding because some CSVs have BOM added to the first key
            with open(path, mode="r", encoding="utf-8-sig") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                self._import_samples_for_csv(csv_reader, filename)

    def _import_samples_for_csv(self, csv_reader, filename):
        for row in csv_reader:
            if row["Exp"] == "":
                continue

            sample = find_sample(
                {
                    "exp_name": row["Exp"],
                    "site_name": row["Site"],
                    "hole_name": row["Hole"],
                    "core_name": row["Core"],
                    "core_type": row["Type"],
                    "section_name": row["Section"],
                    "section_aw": row["A/W"],
                    "sample_name": row["Sample"],
                    "top": row["Top [cm]"],
                    "bottom": row["Bottom [cm]"],
                    "top_depth": row["Top Depth [m]"],
                    "bottom_depth": row["Bottom Depth [m]"],
                    "data_source_notes": filename,
                    "data_source_type": "micropal csv",
                }
            )
            if not sample.first():
                section = find_section(
                    {
                        "exp_name": row["Exp"],
                        "site_name": row["Site"],
                        "hole_name": row["Hole"],
                        "core_name": row["Core"],
                        "core_type": row["Type"],
                        "section_name": row["Section"],
                        "section_aw": row["A/W"],
                    }
                ).first()

                if section:
                    attributes = {
                        "section_id": section["id"],
                        "name": row["Sample"],
                        "top": row["Top [cm]"],
                        "bottom": row["Bottom [cm]"],
                        "top_depth": row["Top Depth [m]"],
                        "bottom_depth": row["Bottom Depth [m]"],
                        "raw_data": row,
                        "data_source_notes": filename,
                        "data_source_type": "micropal csv",
                    }
                    create_sample(attributes)


if __name__ == "__main__":
    fire.Fire(Import_Micropal_CSV)
