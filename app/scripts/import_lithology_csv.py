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
from scripts.import_utils.lithology import (
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


def create_app():
    config_str = "config.DevelopmentConfig"

    app = Flask("console")
    app.config.from_object(config_str)
    db.init_app(app)
    ma.init_app(app)

    return app


app = create_app()
app.app_context().push()


class Import_Lithology_CSV(object):
    def clear_table(self, table):
        db.engine.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE;")

    def import_expeditions(self):
        file = f"{FILE_PATH}/get_expeditions_from_crosswalk/expeditions.csv"

        with open(file, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                create_expedition(row)

        db.session.commit()

    def import_sites(self):
        for path in LITHOLOGY_CSVS:
            with open(path, mode="r") as csv_file:
                filename = path.split("/")[-1]
                csv_reader = csv.DictReader(csv_file)
                unique_values = set()
                for row in csv_reader:
                    if row["Exp"] == "" or row["Site"] == "":
                        continue

                    unique_values.add(f"{row['Exp']}|{row['Site']}")

                for value in unique_values:
                    exp_name, site_name = value.split("|")

                    site = find_site(exp_name, site_name)
                    if not site.first():
                        expedition = find_expedition(exp_name)
                        if expedition:
                            create_site(site_name, expedition.id, filename)

            db.session.commit()

    def import_holes(self):
        for path in LITHOLOGY_CSVS:
            with open(path, mode="r") as csv_file:
                filename = path.split("/")[-1]
                csv_reader = csv.DictReader(csv_file)
                unique_values = set()
                for row in csv_reader:
                    if row["Exp"] == "" or row["Hole"] == "":
                        continue

                    unique_values.add(f"{row['Exp']}|{row['Site']}|{row['Hole']}")

                return
                for value in unique_values:
                    exp_name, site_name, hole_name = value.split("|")

                    hole = find_hole(exp_name, site_name, hole_name)
                    if not hole.first():
                        site = find_site(exp_name, site_name).first()
                        if site:
                            create_hole(hole_name, site["id"], filename)

            db.session.commit()

    def import_cores(self):
        for path in LITHOLOGY_CSVS:
            with open(path, mode="r") as csv_file:
                filename = path.split("/")[-1]
                csv_reader = csv.DictReader(csv_file)
                unique_values = set()
                for row in csv_reader:
                    if row["Exp"] == "" or row["Core"] == "":
                        continue

                    unique_values.add(
                        f"{row['Exp']}|{row['Site']}|{row['Hole']}|"
                        f"{row['Core']}|{row['Type']}"
                    )

                for value in unique_values:
                    exp_name, site_name, hole_name, core_name, core_type = value.split(
                        "|"
                    )

                    core = find_core(
                        exp_name, site_name, hole_name, core_name, core_type
                    )
                    if not core.first():
                        hole = find_hole(exp_name, site_name, hole_name).first()
                        if hole:
                            create_core(core_name, core_type, hole["id"], filename)

            db.session.commit()

    def import_sections(self):
        for path in LITHOLOGY_CSVS:
            with open(path, mode="r") as csv_file:
                filename = path.split("/")[-1]
                csv_reader = csv.DictReader(csv_file)
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
                        exp_name,
                        site_name,
                        hole_name,
                        core_name,
                        core_type,
                        section_name,
                    )
                    if not section.first():
                        core = find_core(
                            exp_name, site_name, hole_name, core_name, core_type
                        ).first()
                        if core:
                            create_section(section_name, core["id"], filename)

            db.session.commit()

    def import_samples(self):
        for path in LITHOLOGY_CSVS:
            with open(path, mode="r") as csv_file:
                filename = path.split("/")[-1]
                csv_reader = csv.DictReader(csv_file)
                unique_values = set()
                for row in csv_reader:
                    if row["Exp"] == "" or row["Sample"] == "":
                        continue

                    unique_values.add(
                        f"{row['Exp']}|{row['Site']}|{row['Hole']}|"
                        f"{row['Core']}|"
                        f"{row['Type']}|{row['Section']}|{row['A/W']}|"
                        f"{row['Sample']}|{row['Top [cm]']}|"
                        f"{row['Bottom [cm]']}|"
                        f"{row['Top Depth [m]']}|{row['Bottom Depth [m]']}|"
                        f"{row['Lithology Prefix']}|"
                        f"{row['Lithology Principal Name']}|"
                        f"{row['Lithology Suffix']}|"
                        f"{row['Minor Lithology Prefix']}|"
                        f"{row['Minor Lithology Name']}|"
                        f"{row['Minor Lithology Suffix']}"
                    )

                for value in unique_values:
                    (
                        exp_name,
                        site_name,
                        hole_name,
                        core_name,
                        core_type,
                        section_name,
                        aw,
                        sample_name,
                        top,
                        bottom,
                        top_depth,
                        bottom_depth,
                        principal_lithology_prefix,
                        principal_lithology_name,
                        principal_lithology_suffix,
                        minor_lithology_prefix,
                        minor_lithology_name,
                        minor_lithology_suffix,
                    ) = value.split("|")
                    raw_data = row

                    sample = find_sample(
                        exp_name,
                        site_name,
                        hole_name,
                        core_name,
                        core_type,
                        section_name,
                        aw,
                        sample_name,
                        top,
                        bottom,
                    )
                    if not sample.first():
                        section = find_section(
                            exp_name,
                            site_name,
                            hole_name,
                            core_name,
                            core_type,
                            section_name,
                        ).first()
                        if section:
                            create_sample(
                                section["id"],
                                sample_name,
                                aw,
                                top,
                                bottom,
                                top_depth,
                                bottom_depth,
                                principal_lithology_prefix,
                                principal_lithology_name,
                                principal_lithology_suffix,
                                minor_lithology_prefix,
                                minor_lithology_name,
                                minor_lithology_suffix,
                                raw_data,
                                filename,
                            )

            db.session.commit()


if __name__ == "__main__":
    fire.Fire(Import_Lithology_CSV)
