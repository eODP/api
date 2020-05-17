import pdb

import pytest

from models.expedition import Expedition
from tests.factories import ExpeditionFactory


def test_GET_expeditions_works_with_no_expedition(client):
    response = client.get("/expeditions")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["data"]) == 0


def test_GET_expeditions_returns_saved_expedition(client):
    ExpeditionFactory(name="123", id=1)
    ExpeditionFactory(name="456", id=2)

    response = client.get("/expeditions")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["data"]) == 2
    assert data["data"][0]["name"] == "123"
    assert data["data"][1]["name"] == "456"
    assert data["data"][0] == {
        "data_source_notes": None,
        "data_source_url": None,
        "id": 1,
        "name": "123",
        "sites": [],
        "workbook_tab_name": None,
    }
