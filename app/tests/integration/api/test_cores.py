from tests.factories import CoreFactory


def test_GET_cores_works_with_no_core(client):
    response = client.get("/api/cores")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 0


def test_GET_cores_returns_saved_core(client):
    core1 = CoreFactory(name="123", id=1)
    core2 = CoreFactory(name="456", id=2)

    response = client.get("/api/cores")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == core1.id
    assert data[0]["name"] == core1.name
    assert data[1]["id"] == core2.id
    assert data[1]["name"] == core2.name


def test_GET_cores_detail_returns_core_based_on_id(client):
    core = CoreFactory(name="123", id=1)

    response = client.get(f"/api/cores/{core.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == core.id
    assert data["name"] == core.name


def test_GET_cores_detail_returns_error_mesage_if_no_match(client):
    response = client.get(f"/api/cores/10")
    data = response.get_json()

    assert response.status_code == 404
    assert data["message"] == "Item not found"
