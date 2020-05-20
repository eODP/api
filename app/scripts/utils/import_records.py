from extension import db
from models.core import Core
from models.expedition import Expedition
from models.hole import Hole
from models.sample import Sample
from models.section import Section
from models.site import Site
from scripts.utils.db_utils import allowed_params, trim_doc_string, add_null_queries


def find_expedition(params):
    return Expedition.query.filter_by(name=params["name"]).first()


def create_expedition(params):
    allowed_attributes = ["name", "workbook_tab_name", "data_source_notes"]
    attributes = allowed_params(allowed_attributes, params)

    record = Expedition(**attributes)
    record.save()


def find_site(params):
    sql = trim_doc_string(
        """
        SELECT sites.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name
    """
    )

    allowed_attributes = ["exp_name", "site_name"]
    attributes = allowed_params(allowed_attributes, params)
    sql = add_null_queries(sql, attributes)
    return db.session.execute(sql, attributes)


def create_site(params):
    allowed_attributes = ["name", "expedition_id", "data_source_notes"]
    attributes = allowed_params(allowed_attributes, params)

    record = Site(**attributes)
    record.save()


def find_hole(params):
    sql = trim_doc_string(
        """
        SELECT holes.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        JOIN holes on holes.site_id = sites.id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name
        AND holes.name = :hole_name
    """
    )

    allowed_attributes = ["exp_name", "site_name", "hole_name"]
    attributes = allowed_params(allowed_attributes, params)
    sql = add_null_queries(sql, attributes)
    return db.session.execute(sql, attributes)


def create_hole(params):
    allowed_attributes = ["name", "site_id", "data_source_notes"]
    attributes = allowed_params(allowed_attributes, params)

    record = Hole(**attributes)
    record.save()


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
        AND cores.type = :core_type
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
    allowed_attributes = ["name", "type", "hole_id", "data_source_notes"]
    attributes = allowed_params(allowed_attributes, params)

    record = Core(**attributes)
    record.save()


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
    """
    )

    allowed_attributes = [
        "exp_name",
        "site_name",
        "hole_name",
        "core_name",
        "core_type",
        "section_name",
    ]
    attributes = allowed_params(allowed_attributes, params)
    sql = add_null_queries(sql, attributes)
    return db.session.execute(sql, attributes)


def create_section(params):
    allowed_attributes = ["name", "core_id", "data_source_notes"]
    attributes = allowed_params(allowed_attributes, params)

    record = Section(**attributes)
    record.save()


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
        AND samples.name = :sample_name
        AND samples.aw = :aw
        AND samples.top = :top
        AND samples.bottom = :bottom
    """
    )

    allowed_attributes = [
        "exp_name",
        "site_name",
        "hole_name",
        "core_name",
        "core_type",
        "section_name",
        "aw",
        "sample_name",
        "top",
        "bottom",
    ]
    attributes = allowed_params(allowed_attributes, params)
    sql = add_null_queries(sql, attributes)
    return db.session.execute(sql, attributes)


def create_sample(params):
    allowed_attributes = [
        "section_id",
        "name",
        "aw",
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
    ]
    attributes = allowed_params(allowed_attributes, params)

    record = Sample(**attributes)
    record.save()
