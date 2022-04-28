import csv
import pandas as pd

from extension import db
from models.core import Core
from models.expedition import Expedition
from models.hole import Hole
from models.sample import Sample
from models.section import Section
from models.site import Site
from models.taxon import Taxon
from models.sample_taxon import SampleTaxon
from models.taxon_crosswalk import TaxonCrosswalk
from scripts.utils.db_utils import allowed_params, trim_doc_string, add_null_queries


def import_expedition_for_csv(csv_reader, filename, dataset):
    unique_values = set()
    for row in csv_reader:
        if row["Exp"] == "":
            continue

        unique_values.add(row["Exp"])

    for exp_name in unique_values:
        expedition = find_expedition({"name": exp_name})
        if not expedition:
            create_expedition({"name": exp_name, "dataset": dataset})


def find_expedition(params):
    allowed_attributes = ["name"]
    attributes = allowed_params(allowed_attributes, params)
    return Expedition.find_by_name(**attributes)


def create_expedition(params):
    allowed_attributes = ["name", "workbook_tab_name", "data_source_notes", "dataset"]
    attributes = allowed_params(allowed_attributes, params)

    record = Expedition(**attributes)
    record.save()


def import_sites_for_csv(csv_reader, filename, dataset):
    unique_values = set()
    for row in csv_reader:
        if row["Exp"] == "":
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
                        "dataset": dataset,
                    }
                )


def find_site(params):
    sql = trim_doc_string(
        """
        SELECT sites.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name;
    """
    )

    allowed_attributes = ["exp_name", "site_name"]
    attributes = allowed_params(allowed_attributes, params)
    sql = add_null_queries(sql, attributes)
    return db.session.execute(sql, attributes)


def create_site(params):
    allowed_attributes = ["name", "expedition_id", "data_source_notes", "dataset"]
    attributes = allowed_params(allowed_attributes, params)

    record = Site(**attributes)
    record.save()


def import_holes_for_csv(csv_reader, filename, dataset):
    unique_values = set()
    for row in csv_reader:
        if row["Exp"] == "":
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
                        "dataset": dataset,
                    }
                )


def find_hole(params):
    sql = trim_doc_string(
        """
        SELECT holes.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        JOIN holes on holes.site_id = sites.id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name
        AND holes.name = :hole_name;
    """
    )

    allowed_attributes = ["exp_name", "site_name", "hole_name"]
    attributes = allowed_params(allowed_attributes, params)
    sql = add_null_queries(sql, attributes)
    return db.session.execute(sql, attributes)


def create_hole(params):
    allowed_attributes = ["name", "site_id", "data_source_notes", "dataset"]
    attributes = allowed_params(allowed_attributes, params)

    record = Hole(**attributes)
    record.save()


def import_cores_for_csv(csv_reader, filename, dataset):
    unique_values = set()
    for row in csv_reader:
        if row["Exp"] == "":
            continue

        unique_values.add(
            f"{row['Exp']}|{row['Site']}|{row['Hole']}|" f"{row['Core']}|{row['Type']}"
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
                {"exp_name": exp_name, "site_name": site_name, "hole_name": hole_name}
            ).first()

            if hole:
                create_core(
                    {
                        "name": core_name,
                        "type": core_type,
                        "hole_id": hole["id"],
                        "data_source_notes": filename,
                        "dataset": dataset,
                    }
                )


def find_core(params):
    sql = trim_doc_string(
        """
        SELECT cores.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        JOIN holes on holes.site_id = sites.id
        JOIN cores on cores.hole_id = holes.id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name
        AND holes.name = :hole_name
        AND cores.name = :core_name
        AND cores.type = :core_type;
    """
    )

    allowed_attributes = [
        "exp_name",
        "site_name",
        "hole_name",
        "core_name",
        "core_type",
    ]
    attributes = allowed_params(allowed_attributes, params)
    sql = add_null_queries(sql, attributes)
    return db.session.execute(sql, attributes)


def create_core(params):
    allowed_attributes = ["name", "type", "hole_id", "data_source_notes", "dataset"]
    attributes = allowed_params(allowed_attributes, params)

    record = Core(**attributes)
    record.save()


def import_sections_for_csv(csv_reader, filename, dataset):
    unique_values = set()
    for row in csv_reader:
        if row["Exp"] == "":
            continue

        unique_values.add(
            f"{row['Exp']}|{row['Site']}|{row['Hole']}|"
            f"{row['Core']}|{row['Type']}|{row['Section']}|{row['A/W']}"
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
        ) = value.split("|")

        section = find_section(
            {
                "exp_name": exp_name,
                "site_name": site_name,
                "hole_name": hole_name,
                "core_name": core_name,
                "core_type": core_type,
                "section_name": section_name,
                "section_aw": aw,
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
                        "aw": aw,
                        "data_source_notes": filename,
                        "dataset": dataset,
                    }
                )


def find_section(params):
    sql = trim_doc_string(
        """
        SELECT sections.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        JOIN holes on holes.site_id = sites.id
        JOIN cores on cores.hole_id = holes.id
        JOIN sections on sections.core_id = cores.id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name
        AND holes.name = :hole_name
        AND cores.name = :core_name
        AND cores.type = :core_type
        AND sections.name = :section_name
        AND sections.aw = :section_aw;
    """
    )

    allowed_attributes = [
        "exp_name",
        "site_name",
        "hole_name",
        "core_name",
        "core_type",
        "section_name",
        "section_aw",
    ]
    attributes = allowed_params(allowed_attributes, params)
    sql = add_null_queries(sql, attributes)
    return db.session.execute(sql, attributes)


def create_section(params):
    allowed_attributes = ["name", "core_id", "aw", "data_source_notes", "dataset"]
    attributes = allowed_params(allowed_attributes, params)

    record = Section(**attributes)
    record.save()


def find_sample_by_eodp_id(params):
    allowed_attributes = ["eodp_id"]
    attributes = allowed_params(allowed_attributes, params)
    return Sample.find_by_eodp_id(**attributes)


def find_sample_taxa_by_ids(params):
    allowed_attributes = ["sample_id", "taxon_id"]
    attributes = allowed_params(allowed_attributes, params)
    return SampleTaxon.find_by_ids(**attributes)


def find_sample(params):
    sql = trim_doc_string(
        """
        SELECT samples.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        JOIN holes on holes.site_id = sites.id
        JOIN cores on cores.hole_id = holes.id
        JOIN sections on sections.core_id = cores.id
        JOIN samples on samples.section_id = sections.id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name
        AND holes.name = :hole_name
        AND cores.name = :core_name
        AND cores.type = :core_type
        AND sections.name = :section_name
        AND sections.aw = :section_aw
        AND samples.name = :sample_name
        AND samples.top = :top
        AND samples.bottom = :bottom
        AND samples.top_depth = :top_depth
        AND samples.bottom_depth = :bottom_depth
        AND samples.data_source_notes = :data_source_notes
        AND samples.data_source_type = :data_source_type;
    """
    )

    allowed_attributes = [
        "exp_name",
        "site_name",
        "hole_name",
        "core_name",
        "core_type",
        "section_name",
        "section_aw",
        "sample_name",
        "top",
        "bottom",
        "top_depth",
        "bottom_depth",
        "data_source_notes",
        "data_source_type",
    ]
    attributes = allowed_params(allowed_attributes, params)
    sql = add_null_queries(sql, attributes)
    return db.session.execute(sql, attributes)


def find_lithology_sample(params):
    sql = trim_doc_string(
        """
        SELECT samples.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        JOIN holes on holes.site_id = sites.id
        JOIN cores on cores.hole_id = holes.id
        JOIN sections on sections.core_id = cores.id
        JOIN samples on samples.section_id = sections.id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name
        AND holes.name = :hole_name
        AND cores.name = :core_name
        AND cores.type = :core_type
        AND sections.name = :section_name
        AND sections.aw = :section_aw
        AND samples.name = :sample_name
        AND samples.top = :top
        AND samples.bottom = :bottom
        AND samples.top_depth = :top_depth
        AND samples.bottom_depth = :bottom_depth
        AND samples.principal_lithology_prefix = :principal_lithology_prefix
        AND samples.principal_lithology_name = :principal_lithology_name
        AND samples.principal_lithology_suffix = :principal_lithology_suffix
        AND samples.minor_lithology_prefix = :minor_lithology_prefix
        AND samples.minor_lithology_name = :minor_lithology_name
        AND samples.minor_lithology_suffix = :minor_lithology_suffix
        AND samples.data_source_notes = :data_source_notes
        AND samples.data_source_type = :data_source_type;
    """
    )

    allowed_attributes = [
        "exp_name",
        "site_name",
        "hole_name",
        "core_name",
        "core_type",
        "section_name",
        "section_aw",
        "sample_name",
        "top",
        "bottom",
        "top_depth",
        "bottom_depth",
        "principal_lithology_prefix",
        "principal_lithology_name",
        "principal_lithology_suffix",
        "minor_lithology_prefix",
        "minor_lithology_name",
        "minor_lithology_suffix",
        "data_source_notes",
        "data_source_type",
    ]
    attributes = allowed_params(allowed_attributes, params)
    sql = add_null_queries(sql, attributes)
    return db.session.execute(sql, attributes)


def create_sample(params):
    allowed_attributes = [
        "section_id",
        "name",
        "top",
        "bottom",
        "top_depth",
        "bottom_depth",
        "principal_lithology_prefix",
        "principal_lithology_name",
        "principal_lithology_suffix",
        "minor_lithology_prefix",
        "minor_lithology_name",
        "minor_lithology_suffix",
        "raw_data",
        "data_source_notes",
        "data_source_type",
        "dataset",
        "eodp_id",
    ]
    attributes = allowed_params(allowed_attributes, params)

    record = Sample(**attributes)
    record.save()


def create_taxon(params):
    allowed_attributes = [
        "name",
        "taxon_group",
        "taxon_name_above_genus",
        "genus_modifier",
        "genus_name",
        "subgenera_modifier",
        "subgenera_name",
        "species_modifier",
        "species_name",
        "subspecies_modifier",
        "subspecies_name",
        "non_taxa_descriptor",
        "pbdb_taxon_id",
        "pbdb_taxon_name",
        "pbdb_taxon_rank",
        "pbdb_data",
    ]
    attributes = allowed_params(allowed_attributes, params)

    record = Taxon(**attributes)
    record.save()


def create_taxon_crosswalk(params):
    allowed_attributes = [
        "taxon_id",
        "original_name",
        "taxon_group",
        "comments_1",
        "comments_2",
        "internal_notes",
        "name_comment",
        "eodp_id",
    ]
    attributes = allowed_params(allowed_attributes, params)

    record = TaxonCrosswalk(**attributes)
    record.save()


def find_taxon_by_name(params):
    allowed_attributes = ["name", "taxon_group"]
    attributes = allowed_params(allowed_attributes, params)
    return Taxon.find_by_name_and_group(**attributes)


def find_taxon_crosswalk_by_name(params):
    allowed_attributes = ["name", "taxon_group"]
    attributes = allowed_params(allowed_attributes, params)
    return TaxonCrosswalk.find_by_name_and_group(**attributes)


def find_taxon_crosswalk_by_name_and_taxon(params):
    allowed_attributes = ["crosswalk_name", "taxon_name", "taxon_group"]
    attributes = allowed_params(allowed_attributes, params)
    return TaxonCrosswalk.find_by_name_and_taxon(**attributes)


def create_sample_taxon(params):
    allowed_attributes = [
        "sample_id",
        "taxon_id",
        "original_taxon_id",
        "code",
        "data_source_notes",
        "dataset",
    ]
    attributes = allowed_params(allowed_attributes, params)

    record = SampleTaxon(**attributes)
    record.save()


def fetch_nontaxa_fields(nontaxa_csv):
    nontaxa_fields = set()

    with open(nontaxa_csv, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            nontaxa_fields.add(row["original"])

    return nontaxa_fields


def fetch_file_taxon_groups(metadata_csvs):
    taxon_groups = {}

    for path in metadata_csvs:
        with open(path, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                taxon_groups[row["file"]] = row["taxon_group"]

    return taxon_groups


def process_taxa_crosswalk_file(path):
    df = pd.read_csv(path, dtype=str)
    all_verbatim_names = {}
    for index, row in df.iterrows():
        if row["verbatim_name"] not in all_verbatim_names:
            all_verbatim_names[row["verbatim_name"].strip()] = []

        if row["taxon_group"] not in all_verbatim_names[row["verbatim_name"]]:
            all_verbatim_names[row["verbatim_name"]].append(row["taxon_group"])
    return all_verbatim_names


def fetch_taxa_ids(verbatim_names, taxa_names):
    taxa_dict = {}
    for name in taxa_names:
        taxon_groups = verbatim_names[name]
        for taxon_group in taxon_groups:
            if taxon_group == taxon_group:
                taxon = find_taxon_crosswalk_by_name(
                    {"name": name.strip(), "taxon_group": taxon_group}
                )
            else:
                taxon = find_taxon_crosswalk_by_name({"name": name.strip()})
            if taxon is None:
                continue

            taxa_dict[name] = {
                "taxon_id": taxon.taxon_id,
                "original_taxon_id": taxon.id,
            }

    return taxa_dict
