import os

import pdb
import pytest

from models.expedition import Expedition
from extension import db
from app import create_app


@pytest.fixture()
def create_expedition():
    def factory(
        name="name",
        data_source_notes="data_source_notes",
        data_source_url="data_source_url",
        workbook_tab_name="workbook_tab_name",
    ):
        exp = Expedition(
            name=name,
            data_source_notes=data_source_notes,
            data_source_url=data_source_url,
            workbook_tab_name=workbook_tab_name,
        )

        exp.save()
        return exp

    return factory


@pytest.fixture(scope="module")
def app():
    os.environ["ENV"] = "Testing"
    return create_app()


@pytest.fixture()
def client(app):
    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            yield test_client
            # Must remove session before dropping all tables for postgres
            # https://stackoverflow.com/a/55557351
            db.session.remove()
            db.drop_all()
