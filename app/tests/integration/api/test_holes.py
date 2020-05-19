from tests.factories import HoleFactory


def test_GET_holes_works_with_no_hole(client):
    response = client.get("/holes")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 0


def test_GET_holes_returns_saved_hole(client):
    hole1 = HoleFactory(name="123", id=1)
    hole2 = HoleFactory(name="456", id=2)

    response = client.get("/holes")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == hole1.id
    assert data[0]["name"] == hole1.name
    assert data[1]["id"] == hole2.id
    assert data[1]["name"] == hole2.name


def test_GET_holes_detail_returns_hole_based_on_id(client):
    hole = HoleFactory(name="123", id=1)

    response = client.get(f"/holes/{hole.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == hole.id
    assert data["name"] == hole.name


def test_GET_holes_detail_returns_error_mesage_if_no_match(client):
    response = client.get(f"/holes/10")
    data = response.get_json()

    assert response.status_code == 404
    assert data["message"] == "Item not found"
