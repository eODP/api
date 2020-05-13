import os, sys
import csv
import glob
import pdb
import json

import pandas as pd
import click
from flask import Flask
from flask.cli import FlaskGroup
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)
path = os.environ.get("PASSENGER_BASE_PATH")
sys.path.append(path)

from extension import db, ma
from models.core import CoreModel
from models.expedition import ExpeditionModel
from models.hole import HoleModel
from models.sample_taxon import SampleTaxonModel
from models.sample import SampleModel
from models.section import SectionModel
from models.site import SiteModel
from models.taxon import TaxonModel

FILE_PATH = os.environ.get("RAW_DATA_PATH")
LITHOLOGY_CSVS = glob.glob(f"{FILE_PATH}/Lithology_CSV/*.csv")


def create_app():
    config_str = "config.DevelopmentConfig"

    app = Flask('console')
    app.config.from_object(config_str)
    db.init_app(app)
    ma.init_app(app)

    return app

app = create_app()


@app.cli.command("clear_table")
@click.argument("table")
def clear_table(table):
     db.engine.execute(f"DELETE FROM {table};")


@app.cli.command("import_expeditions")
def import_expeditions():
    file = f"{FILE_PATH}/get_expeditions_from_crosswalk/expeditions.csv"

    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            record = ExpeditionModel(
                name = row['name'],
                data_source_notes = row['data_source_notes'],
                workbook_tab_name = row['workbook_tab_name']
            )

            db.session.add(record)

    db.session.commit()

def find_site(exp_name, site_name):
    sql = """
        SELECT sites.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name
    """
    return db.session.execute(
        sql,
        {'exp_name': exp_name, 'site_name': site_name}
    )

def find_expedition(exp_name):
    return ExpeditionModel.query.filter_by(name = exp_name).first()

def create_site(site_name, expedition_id):
    record = SiteModel(name = site_name, expedition_id = expedition_id)
    db.session.add(record)

@app.cli.command("import_sites")
def import_sites():
    for path in LITHOLOGY_CSVS:
        with open(path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            unique_values = set()
            for row in csv_reader:
                unique_values.add(f"{row['Exp']}|{row['Site']}")

            for value in unique_values:
                exp_name, site_name = value.split('|')

                if exp_name == '' or site_name == '':
                    continue

                site = find_site(exp_name, site_name)
                if not site.first():
                    expedition = find_expedition(exp_name)
                    if expedition:
                        create_site(site_name, expedition.id)

        db.session.commit()


def find_hole(exp_name, site_name, hole_name):
    sql = """
        SELECT holes.*
        FROM expeditions
        JOIN sites ON expeditions.id = sites.expedition_id
        JOIN holes on holes.site_id = sites.id
        WHERE expeditions.name = :exp_name
        AND sites.name = :site_name
        AND holes.name = :hole_name
    """
    return db.session.execute(
        sql,
        {'exp_name': exp_name, 'site_name': site_name, 'hole_name': hole_name}
    )

def create_hole(hole_name, site_id):
    record = HoleModel(name = hole_name, site_id = site_id)
    db.session.add(record)

@app.cli.command("import_holes")
def import_holes():
    for path in LITHOLOGY_CSVS:
        with open(path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            unique_values = set()
            for row in csv_reader:
                unique_values.add(f"{row['Exp']}|{row['Site']}|{row['Hole']}")

            for value in unique_values:
                exp_name, site_name, hole_name = value.split('|')

                if exp_name == '' or hole_name == '':
                    continue

                hole = find_hole(exp_name, site_name, hole_name)
                if not hole.first():
                    site = find_site(exp_name, site_name).first()
                    if site:
                        create_hole(hole_name, site['id'])

        db.session.commit()


def find_core(exp_name, site_name, hole_name, core_name, core_type):
    sql = """
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
    return db.session.execute(
        sql,
        {
            'exp_name': exp_name, 'site_name': site_name,
            'hole_name': hole_name, 'core_name': core_name,
            'core_type': core_type
        }
    )

def create_core(core_name, core_type, hole_id):
    record = CoreModel(name = core_name, type = core_type, hole_id = hole_id)
    db.session.add(record)


@app.cli.command("import_cores")
def import_cores():
    for path in LITHOLOGY_CSVS:
        with open(path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            unique_values = set()
            for row in csv_reader:
                unique_values.add(
                    f"{row['Exp']}|{row['Site']}|{row['Hole']}|{row['Core']}|" \
                    f"{row['Type']}"
                )

            for value in unique_values:
                exp_name, site_name, hole_name, core_name, core_type = value.split('|')

                if exp_name == '' or core_name == '':
                    continue

                core = find_core(exp_name, site_name, hole_name, core_name,
                                 core_type)
                if not core.first():
                    hole = find_hole(exp_name, site_name, hole_name).first()
                    if hole:
                        create_core(core_name, core_type, hole['id'])

        db.session.commit()


def find_section(exp_name, site_name, hole_name, core_name, core_type,
                 section_name):
    sql = """
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
    return db.session.execute(
        sql,
        {
            'exp_name': exp_name, 'site_name': site_name,
            'hole_name': hole_name, 'core_name': core_name,
            'core_type': core_type, 'section_name': section_name
        }
    )

def create_section(section_name, core_id):
    record = SectionModel(name = section_name, core_id = core_id)
    db.session.add(record)


@app.cli.command("import_sections")
def import_sections():
    for path in LITHOLOGY_CSVS:
        with open(path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            unique_values = set()
            for row in csv_reader:
                unique_values.add(
                    f"{row['Exp']}|{row['Site']}|{row['Hole']}|{row['Core']}|" \
                    f"{row['Type']}|{row['Section']}"
                )

            for value in unique_values:
                exp_name, site_name, hole_name, core_name, core_type, section_name = value.split('|')

                if exp_name == '' or section_name == '':
                    continue

                section = find_section(exp_name, site_name, hole_name,
                                       core_name, core_type, section_name)
                if not section.first():
                    core = find_core(exp_name, site_name, hole_name, core_name,
                                     core_type).first()
                    if core:
                        create_section(section_name, core['id'])

        db.session.commit()


def find_sample(exp_name, site_name, hole_name, core_name, core_type,
                section_name, aw, sample_name, top, bottom):
    sql = """
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

def create_sample(section_id, sample_name, aw, top, bottom, top_depth, bottom_depth,
    principal_lithology_prefix, principal_lithology_name,
    principal_lithology_suffix, minor_lithology_prefix,
    minor_lithology_name, minor_lithology_suffix, raw_data):
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
        raw_data =  raw_data
    )
    db.session.add(record)


@app.cli.command("import_samples")
def import_samples():
    for path in LITHOLOGY_CSVS:
        with open(path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            unique_values = set()
            for row in csv_reader:
                unique_values.add(
                    f"{row['Exp']}|{row['Site']}|{row['Hole']}|{row['Core']}|" \
                    f"{row['Type']}|{row['Section']}|{row['A/W']}|" \
                    f"{row['Sample']}|{row['Top [cm]']}|{row['Bottom [cm]']}|" \
                    f"{row['Top Depth [m]']}|{row['Bottom Depth [m]']}|" \
                    f"{row['Lithology Prefix']}|" \
                    f"{row['Lithology Principal Name']}|" \
                    f"{row['Lithology Suffix']}|" \
                    f"{row['Minor Lithology Prefix']}|" \
                    f"{row['Minor Lithology Name']}|" \
                    f"{row['Minor Lithology Suffix']}"
                )

            for value in unique_values:
                exp_name, site_name, hole_name, core_name, core_type, section_name, aw, sample_name, top, bottom, top_depth, bottom_depth,  principal_lithology_prefix, principal_lithology_name, principal_lithology_suffix,  minor_lithology_prefix, minor_lithology_name, minor_lithology_suffix = value.split('|')
                raw_data = row

                if exp_name == '' or sample_name == '':
                    continue

                sample = find_sample(exp_name, site_name, hole_name, core_name,
                                     core_type, section_name, aw,
                                     sample_name, top, bottom)
                if not sample.first():
                    section = find_section(exp_name, site_name, hole_name,
                                           core_name, core_type, section_name).first()
                    if section:
                        create_sample(section['id'], sample_name, aw,
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
                            raw_data)

        db.session.commit()


