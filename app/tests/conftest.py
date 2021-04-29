import os
import sys

import pytest
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)
path = os.environ.get("PASSENGER_BASE_PATH")
sys.path.append(path)


from extension import db
from app import create_app


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
            # Must remove session before dropping all tables for postgresql
            # https://stackoverflow.com/a/55557351
            db.session.remove()
            db.drop_all()
