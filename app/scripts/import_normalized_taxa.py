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
    find_sample,
    find_taxon_by_name,
    create_taxon,
    create_sample_taxon,
    create_taxon_crosswalk,
    fetch_taxa_columns,
    fetch_taxa_ids,
    fetch_nontaxa_fields,
)

TAXON_GROUP = "nannofossils"
FILE_PATH = os.environ.get("RAW_DATA_PATH")
MICROPAL_CSVS = glob.glob(f"{FILE_PATH}/Micropal_CSV_1/*.csv")
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/Micropal_CSV_2/*.csv"))
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/Micropal_CSV_3/*.csv"))
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/Micropal_CSV_revised/*.csv"))

DATE = "2021-03-01"
TAXA_CSV = f"{FILE_PATH}/taxa/taxa_list_{TAXON_GROUP}_{DATE}.csv"
TAXA_CROSSWALK_CSV = f"{FILE_PATH}/taxa/taxa_crosswalk_{TAXON_GROUP}_{DATE}.csv"
NONTAXA_CSV = f"{FILE_PATH}/taxa/non_taxa_fields_normalized.csv"
METADATA_CSVS = [
    f"{FILE_PATH}/metadata/Micropal_1_changes.csv",
    f"{FILE_PATH}/metadata/Micropal_2_changes.csv",
    f"{FILE_PATH}/metadata/Micropal_3_changes.csv",
    f"{FILE_PATH}/metadata/Micropal_revised_changes.csv",
]

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
                create_taxon(
                    {
                        "name": row["normalized_name"],
                        "taxon_group": row["taxon_group"],
                        "taxon_name_above_genus": row["Any taxon above genus"],
                        "genus_modifier": row["genus modifier"],
                        "genus_name": row["genus name"],
                        "subgenera_modifier": row["subgenera modifier"],
                        "subgenera_name": row["subgenera name"],
                        "species_modifier": row["species modifier"],
                        "species_name": row["species name"],
                        "subspecies_modifier": row["subspecies modifier"],
                        "subspecies_name": row["subspecies name"],
                        "non_taxa_descriptor": row["non-taxa descriptor"],
                        "comments": row["comments"],
                    }
                )

    def import_taxa_crosswalk(self):
        with open(TAXA_CROSSWALK_CSV, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                taxon = find_taxon_by_name(
                    {
                        "name": row["normalized_name"],
                        "taxon_group": row["taxon_group"],
                        "comments": row["comments"],
                    }
                )

                create_taxon_crosswalk(
                    {
                        "taxon_id": taxon.id,
                        "taxon_group": row["taxon_group"],
                        "original_name": row["verbatim_name"].strip(),
                    }
                )

    def import_sample_taxa(self):
        nontaxa_fields = fetch_nontaxa_fields(NONTAXA_CSV)

        for path in MICROPAL_CSVS:

            filename = path.split("/")[-1]
            print(filename)
            taxon_group = TAXON_GROUP

            with open(path, mode="r", encoding="utf-8-sig") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                taxa_columns = fetch_taxa_columns(csv_reader, nontaxa_fields)

            with open(path, mode="r", encoding="utf-8-sig") as csv_file:
                csv_reader = csv.DictReader(csv_file)

                taxa_ids = fetch_taxa_ids(taxon_group, taxa_columns)
                if bool(taxa_ids):
                    self._import_sample_taxa_for_csv(
                        csv_reader, filename, taxon_group, taxa_ids
                    )

    def _import_sample_taxa_for_csv(self, csv_reader, filename, taxon_group, taxa_ids):
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

            sample = sample.first()

            if sample:
                sample_id = sample.id
                for name, ids in taxa_ids.items():
                    taxon_code = row[name]
                    if taxon_code:
                        create_sample_taxon(
                            {
                                "original_taxon_id": ids["original_taxon_id"],
                                "taxon_id": ids["taxon_id"],
                                "sample_id": sample_id,
                                "code": taxon_code,
                                "data_source_notes": filename,
                            }
                        )

            else:
                raise ValueError(f"Invalid sample {row['Sample']} {row['Exp']}")


if __name__ == "__main__":
    fire.Fire(Import_Normalized_Taxa)
