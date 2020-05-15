import os, sys

from dotenv import load_dotenv

load_dotenv(".env", verbose=True)
path = os.environ.get("PASSENGER_BASE_PATH")
sys.path.append(path)

from extension import db
from models.core import CoreModel
from models.expedition import ExpeditionModel
from models.hole import HoleModel
from models.sample_taxon import SampleTaxonModel
from models.sample import SampleModel
from models.section import SectionModel
from models.site import SiteModel
from models.taxon import TaxonModel

def trim(string):
    return string.replace('\n', ' ').replace('  ', '')

def find_expedition(exp_name):
    return ExpeditionModel.query.filter_by(name = exp_name).first()

def create_expedition(row):
    record = ExpeditionModel(
        name = row['name'],
        data_source_notes = row['data_source_notes'],
        workbook_tab_name = row['workbook_tab_name']
    )
    db.session.add(record)

def find_site(exp_name, site_name):
    sql = trim("""
        SELECT sites.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name
    """)

    return db.session.execute(
        sql,
        {'exp_name': exp_name, 'site_name': site_name}
    )

def create_site(site_name, expedition_id, data_source_notes):
    record = SiteModel(
        name = site_name, expedition_id = expedition_id,
        data_source_notes = data_source_notes
    )
    db.session.add(record)

def find_hole(exp_name, site_name, hole_name):
    sql = trim("""
        SELECT holes.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        JOIN holes on holes.site_id = sites.id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name
        AND holes.name = :hole_name
    """)

    return db.session.execute(
        sql,
        {'exp_name': exp_name, 'site_name': site_name, 'hole_name': hole_name}
    )

def create_hole(hole_name, site_id, data_source_notes):
    record = HoleModel(
        name = hole_name, site_id = site_id,
        data_source_notes = data_source_notes
    )
    db.session.add(record)

def find_core(exp_name, site_name, hole_name, core_name, core_type):
    sql = trim("""
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
    """)

    return db.session.execute(
        sql,
        {
            'exp_name': exp_name, 'site_name': site_name,
            'hole_name': hole_name, 'core_name': core_name,
            'core_type': core_type
        }
    )

def create_core(core_name, core_type, hole_id, data_source_notes):
    record = CoreModel(
        name = core_name, type = core_type, hole_id = hole_id,
        data_source_notes = data_source_notes
    )
    db.session.add(record)

def find_section(exp_name, site_name, hole_name, core_name, core_type,
                 section_name):
    sql = trim("""
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
    """)

    return db.session.execute(
        sql,
        {
            'exp_name': exp_name, 'site_name': site_name,
            'hole_name': hole_name, 'core_name': core_name,
            'core_type': core_type, 'section_name': section_name
        }
    )

def create_section(section_name, core_id, data_source_notes):
    record = SectionModel(
        name = section_name, core_id = core_id,
        data_source_notes = data_source_notes
    )
    db.session.add(record)

def find_sample(exp_name, site_name, hole_name, core_name, core_type,
                section_name, aw, sample_name, top, bottom):
    sql = trim("""
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
    """)

    top = None if top == '' else top
    bottom = None if bottom == '' else bottom

    return db.session.execute(
        sql,
        {
            'exp_name': exp_name, 'site_name': site_name,
            'hole_name': hole_name, 'core_name': core_name,
            'core_type': core_type, 'section_name': section_name,
            'aw': aw, 'sample_name': sample_name, 'top': top, 'bottom': bottom
        }
    )

def create_sample(section_id, sample_name, aw, top, bottom, top_depth,
    bottom_depth, principal_lithology_prefix, principal_lithology_name,
    principal_lithology_suffix, minor_lithology_prefix,
    minor_lithology_name, minor_lithology_suffix, raw_data, data_source_notes):

    top = None if top == '' else top
    bottom = None if bottom == '' else bottom
    top_depth = None if top_depth == '' else top_depth
    bottom_depth = None if bottom_depth == '' else bottom_depth

    record = SampleModel(
        section_id = section_id,
        name = sample_name,
        aw = aw,
        top = top,
        bottom = bottom,
        top_depth = top_depth,
        bottom_depth = bottom_depth,
        principal_lithology_prefix = principal_lithology_prefix,
        principal_lithology_name = principal_lithology_name,
        principal_lithology_suffix = principal_lithology_suffix,
        minor_lithology_prefix = minor_lithology_prefix,
        minor_lithology_name = minor_lithology_name,
        minor_lithology_suffix = minor_lithology_suffix,
        raw_data =  raw_data,
        data_source_notes = data_source_notes
    )
    db.session.add(record)


