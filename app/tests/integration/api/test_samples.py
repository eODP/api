from tests.factories import SampleFactory


def test_GET_samples_works_with_no_sample(client):
    response = client.get("/api/samples")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 0


def test_GET_samples_returns_saved_sample(client):
    sample1 = SampleFactory(name="123", id=1)
    sample2 = SampleFactory(name="456", id=2)

    response = client.get("/api/samples")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == sample1.id
    assert data[0]["name"] == sample1.name
    assert data[1]["id"] == sample2.id
    assert data[1]["name"] == sample2.name


def test_GET_samples_detail_returns_sample_based_on_id(client):
    sample = SampleFactory(name="123", id=1)

    response = client.get(f"/api/samples/{sample.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == sample.id
    assert data["name"] == sample.name


def test_GET_samples_detail_returns_error_mesage_if_no_match(client):
    response = client.get(f"/api/samples/10")
    data = response.get_json()

    assert response.status_code == 404
    assert data["message"] == "Item not found"
