from tests.factories import ExpeditionFactory


def test_GET_expeditions_works_with_no_expedition(client):
    response = client.get("/api/expeditions")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 0


def test_GET_expeditions_returns_saved_expedition(client):
    exp1 = ExpeditionFactory(name="123", id=1)
    exp2 = ExpeditionFactory(name="456", id=2)

    response = client.get("/api/expeditions")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == exp1.id
    assert data[0]["name"] == exp1.name
    assert data[1]["id"] == exp2.id
    assert data[1]["name"] == exp2.name


def test_GET_expeditions_detail_returns_expedition_based_on_id(client):
    exp = ExpeditionFactory(name="123", id=1)

    response = client.get(f"/api/expeditions/{exp.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == exp.id
    assert data["name"] == exp.name


def test_GET_expeditions_detail_returns_error_mesage_if_no_match(client):
    response = client.get(f"/api/expeditions/10")
    data = response.get_json()

    assert response.status_code == 404
    assert data["message"] == "Item not found"
