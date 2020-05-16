import os
import sys
import csv
import glob
import pdb

from flask import Flask
import fire
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)
path = os.environ.get("PASSENGER_BASE_PATH")
sys.path.append(path)

from extension import db, ma
from scripts.utils.import_records import (
    find_expedition,
    create_expedition,
    find_site,
    create_site,
    find_hole,
    create_hole,
    find_core,
    create_core,
    find_section,
    create_section,
    find_sample,
    create_sample,
)

FILE_PATH = os.environ.get("RAW_DATA_PATH")
LITHOLOGY_CSVS = glob.glob(f"{FILE_PATH}/Lithology_CSV/*.csv")

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


class Import_Lithology_CSV(object):
    def clear_table(self, table):
        db.engine.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE;")

    def import_expeditions(self):
        file = f"{FILE_PATH}/get_expeditions_from_crosswalk/expeditions.csv"

        with open(file, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                create_expedition(row)

    def import_sites(self):
        for path in LITHOLOGY_CSVS:
            filename = path.split("/")[-1]
            with open(path, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                self.import_sites_for_csv(csv_reader, filename)

    def import_sites_for_csv(self, csv_reader, filename):
        unique_values = set()
        for row in csv_reader:
            if row["Exp"] == "" or row["Site"] == "":
                continue

            unique_values.add(f"{row['Exp']}|{row['Site']}")

        for value in unique_values:
            exp_name, site_name = value.split("|")

            site = find_site({"exp_name": exp_name, "site_name": site_name})
            if not site.first():
                expedition = find_expedition({"name": exp_name})

                if expedition:
                    create_site(
                        {
                            "name": site_name,
                            "expedition_id": expedition.id,
                            "data_source_notes": filename,
                        }
                    )

    def import_holes(self):
        for path in LITHOLOGY_CSVS:
            filename = path.split("/")[-1]
            with open(path, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                self.import_holes_for_csv(csv_reader, filename)

    def import_holes_for_csv(self, csv_reader, filename):
        unique_values = set()
        for row in csv_reader:
            if row["Exp"] == "" or row["Hole"] == "":
                continue

            unique_values.add(f"{row['Exp']}|{row['Site']}|{row['Hole']}")

        for value in unique_values:
            exp_name, site_name, hole_name = value.split("|")

            hole = find_hole(
                {"exp_name": exp_name, "site_name": site_name, "hole_name": hole_name}
            )
            if not hole.first():
                site = find_site({"exp_name": exp_name, "site_name": site_name}).first()

                if site:
                    create_hole(
                        {
                            "name": hole_name,
                            "site_id": site["id"],
                            "data_source_notes": filename,
                        }
                    )

    def import_cores(self):
        for path in LITHOLOGY_CSVS:
            filename = path.split("/")[-1]
            with open(path, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                self.import_cores_for_csv(csv_reader, filename)

    def import_cores_for_csv(self, csv_reader, filename):
        unique_values = set()
        for row in csv_reader:
            if row["Exp"] == "" or row["Core"] == "":
                continue

            unique_values.add(
                f"{row['Exp']}|{row['Site']}|{row['Hole']}|"
                f"{row['Core']}|{row['Type']}"
            )

        for value in unique_values:
            exp_name, site_name, hole_name, core_name, core_type = value.split("|")

            core = find_core(
                {
                    "exp_name": exp_name,
                    "site_name": site_name,
                    "hole_name": hole_name,
                    "core_name": core_name,
                    "core_type": core_type,
                }
            )
            if not core.first():
                hole = find_hole(
                    {
                        "exp_name": exp_name,
                        "site_name": site_name,
                        "hole_name": hole_name,
                    }
                ).first()

                if hole:
                    create_core(
                        {
                            "name": core_name,
                            "type": core_type,
                            "hole_id": hole["id"],
                            "data_source_notes": filename,
                        }
                    )

    def import_sections(self):
        for path in LITHOLOGY_CSVS:
            filename = path.split("/")[-1]
            with open(path, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                self.import_sections_for_csv(csv_reader, filename)

    def import_sections_for_csv(self, csv_reader, filename):
        unique_values = set()
        for row in csv_reader:
            if row["Exp"] == "" or row["Section"] == "":
                continue

            unique_values.add(
                f"{row['Exp']}|{row['Site']}|{row['Hole']}|"
                f"{row['Core']}|{row['Type']}|{row['Section']}"
            )

        for value in unique_values:
            (
                exp_name,
                site_name,
                hole_name,
                core_name,
                core_type,
                section_name,
            ) = value.split("|")

            section = find_section(
                {
                    "exp_name": exp_name,
                    "site_name": site_name,
                    "hole_name": hole_name,
                    "core_name": core_name,
                    "core_type": core_type,
                    "section_name": section_name,
                }
            )
            if not section.first():
                core = find_core(
                    {
                        "exp_name": exp_name,
                        "site_name": site_name,
                        "hole_name": hole_name,
                        "core_name": core_name,
                        "core_type": core_type,
                    }
                ).first()

                if core:
                    create_section(
                        {
                            "name": section_name,
                            "core_id": core["id"],
                            "data_source_notes": filename,
                        }
                    )

    def import_samples(self):
        for path in LITHOLOGY_CSVS:
            filename = path.split("/")[-1]
            with open(path, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                self.import_samples_for_csv(csv_reader, filename)

    def import_samples_for_csv(self, csv_reader, filename):
        for row in csv_reader:
            if row["Exp"] == "" or row["Sample"] == "":
                continue

            sample = find_sample(
                {
                    "exp_name": row["Exp"],
                    "site_name": row["Site"],
                    "hole_name": row["Hole"],
                    "core_name": row["Core"],
                    "core_type": row["Type"],
                    "section_name": row["Section"],
                    "aw": row["A/W"],
                    "sample_name": row["Sample"],
                    "top": row["Top [cm]"],
                    "bottom": row["Bottom [cm]"],
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
                    }
                ).first()

                if section:
                    attributes = {
                        "section_id": section["id"],
                        "name": row["Sample"],
                        "aw": row["A/W"],
                        "top": row["Top [cm]"],
                        "bottom": row["Bottom [cm]"],
                        "top_depth": row["Top Depth [m]"],
                        "bottom_depth": row["Bottom Depth [m]"],
                        "principal_lithology_prefix": row["Lithology Prefix"],
                        "principal_lithology_name": row["Lithology Principal Name"],
                        "principal_lithology_suffix": row["Lithology Suffix"],
                        "minor_lithology_prefix": row["Minor Lithology Prefix"],
                        "minor_lithology_name": row["Minor Lithology Name"],
                        "minor_lithology_suffix": row["Minor Lithology Suffix"],
                        "raw_data": row,
                        "data_source_notes": filename,
                    }
                    create_sample(attributes)


if __name__ == "__main__":
    fire.Fire(Import_Lithology_CSV)
