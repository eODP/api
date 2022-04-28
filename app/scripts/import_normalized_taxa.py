import os
import csv
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
    find_sample_by_eodp_id,
    find_taxon_by_name,
    find_taxon_crosswalk_by_name_and_taxon,
    create_taxon,
    create_sample_taxon,
    create_taxon_crosswalk,
    fetch_taxa_ids,
    find_sample_taxa_by_ids,
    process_taxa_crosswalk_file
)
from scripts.utils.pbdb_utils import format_pbdb_data_for_row

taxon_groups = [
    "nannofossils",
    "silicoflagellates",
    "ostracods",
    "ebridians",
    "chrysophyte_cysts",
    "bolboformids",
    "diatoms",
    "planktic_forams",
    "radiolarians",
    "dinoflagellates",
    "palynology",
    "benthic_forams",
]

FILE_PATH = os.environ.get("CLEANED_DATA_PATH")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH")

MICROPAL_CSVS = glob.glob(f"{FILE_PATH}/LIMS/Micropal_CSV_1/*.csv")
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/LIMS/Micropal_CSV_2/*.csv"))
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/LIMS/Micropal_CSV_3/*.csv"))
MICROPAL_CSVS.extend(glob.glob(f"{FILE_PATH}/LIMS/Micropal_CSV_revised/*.csv"))


DATE = "2022-04-28"
TAXA_PATH = f"{OUTPUT_PATH}/taxa/LIMS/taxa_list_{DATE}.csv"
TAXA_CROSSWALK_PATH = f"{OUTPUT_PATH}/taxa/LIMS/taxa_crosswalk_{DATE}.csv"
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


class Import_Normalized_Taxa(object):
    def clear_table(self, table):
        db.engine.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE;")

    def import_taxa(self):
        self._import_taxa_file(TAXA_PATH)

    def _import_taxa_file(self, path):
        with open(path, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                taxon = find_taxon_by_name(
                    {
                        "name": row["normalized_name"].strip(),
                        "taxon_group": row["taxon_group"].strip(),
                    }
                )

                if taxon is None:
                    data = {
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
                        "pbdb_taxon_id": row['pbdb_taxon_id'],
                        "pbdb_taxon_name": row['pbdb_taxon_name'],
                        "pbdb_taxon_rank": row['pbdb_taxon_rank']
                    }
                    pbdb_data = format_pbdb_data_for_row(row)
                    if pbdb_data:
                        data['pbdb_data'] = pbdb_data

                    create_taxon(data)

    def import_taxa_crosswalk(self):
        dex_sin_taxa = [
            "Dextral:Sinistral _N. acostaensis_",
            "Dextral:Sinistral _P. finalis_",
            "Dextral:Sinistral _P. obliquiloculata_",
            "Dextral:Sinistral _P. praecursor_",
            "Dextral:Sinistral _P. praespectabilis_",
            "Dextral:Sinistral _P. primalis_",
            "Dextral:Sinistral _P. spectabilis_"
        ]
        with open(TAXA_CROSSWALK_PATH, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                verbatim_name = row["verbatim_name"].strip()
                if verbatim_name in dex_sin_taxa:
                    row["verbatim_name"] = row['normalized_name']
                    self._import_taxa_crosswalk_file(row)
                else:
                    self._import_taxa_crosswalk_file(row)

    def _import_taxa_crosswalk_file(self, row):
        taxon_crosswalk = find_taxon_crosswalk_by_name_and_taxon(
            {
                "crosswalk_name": row["verbatim_name"],
                "taxon_name": row["normalized_name"],
                "taxon_group": row["taxon_group"],
            }
        )
        if taxon_crosswalk is None:
            taxon = find_taxon_by_name(
                {
                    "name": row["normalized_name"].strip(),
                    "taxon_group": row["taxon_group"].strip(),
                }
            )
            if taxon is None:
                raise ValueError(f'<{row["normalized_name"]}:{row["taxon_group"]}> is not in DB')

            create_taxon_crosswalk(
                {
                    "taxon_id": taxon.id,
                    "taxon_group": row["taxon_group"],
                    "original_name": row["verbatim_name"],
                    "comments_1": row["Comment"],
                    "comments_2": row["comments"],
                    "internal_notes": row["Notes (change to Internal only notes?)"],
                    "name_comment": row["name comment field"],
                    "eodp_id": row["eodp_id"]
                }
            )

    def import_sample_taxa(self):
        all_verbatim_names = process_taxa_crosswalk_file(TAXA_CROSSWALK_PATH)
        for path in MICROPAL_CSVS:
            # if '320_U1331B_Radiolarians_2.csv' not in path:
            #     continue
            print(path)
            filename = path.split("cleaned_data/")[-1]
            df = pd.read_csv(path, dtype=str)
            df.dropna(how='all', axis=1, inplace=True)
            df.dropna(how='all', axis=0, inplace=True)

            # get all the taxa names in the file headers
            columns = [col.strip() for col in df.columns]
            file_taxa = set(columns).intersection(set(all_verbatim_names.keys()))
            taxa_ids = fetch_taxa_ids(all_verbatim_names, file_taxa)

            if len(file_taxa) > 0:
                self._import_sample_taxa_for_csv(df, filename, taxa_ids)

    def _import_sample_taxa_for_csv(self, df, filename, taxa_ids):
        for index, row in df.iterrows():
            if row["Exp"] == "":
                continue

            sample = find_sample_by_eodp_id(
                {
                    "eodp_id": row['eodp_id']
                }
            )
            if sample:
                for taxon_name, ids in taxa_ids.items():
                    matching_taxa = []
                    for col in row.keys():
                        if col.strip() == taxon_name:
                            matching_taxa.append(col)
                    if len(matching_taxa) > 1:
                        print(f'{filename} {taxon_name} more than one match.')

                    taxon_code = row[matching_taxa[0]]
                    if taxon_code == taxon_code:
                        sample_taxon = find_sample_taxa_by_ids({
                            "taxon_id": ids["taxon_id"],
                            "sample_id": sample.id,
                        })
                        if sample_taxon is None:
                            attr = {
                                "original_taxon_id": ids["original_taxon_id"],
                                "taxon_id": ids["taxon_id"],
                                "sample_id": sample.id,
                                "data_source_notes": filename,
                                "dataset": DATASET,
                            }
                            if taxon_code != 'eODP_NA':
                                attr['code'] = taxon_code
                            create_sample_taxon(attr)

            else:
                raise ValueError(f"Invalid sample {row['Sample']} {row['Exp']}")


if __name__ == "__main__":
    fire.Fire(Import_Normalized_Taxa)
