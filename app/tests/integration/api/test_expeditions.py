import pdb

import pytest

from models.expedition import Expedition


def test_GET_expeditions_works_with_no_expedition(client):
    response = client.get("/expeditions")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["data"]) == 0


def test_GET_expeditions_returns_saved_expedition(client, create_expedition):
    create_expedition(name="first")
    create_expedition(name="second")

    response = client.get("/expeditions")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["data"]) == 2
    assert data["data"][0]["name"] == "first"
    assert data["data"][1]["name"] == "second"
