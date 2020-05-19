from tests.factories import SiteFactory


def test_GET_sites_works_with_no_site(client):
    response = client.get("/sites")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 0


def test_GET_sites_returns_saved_site(client):
    site1 = SiteFactory(name="123", id=1)
    site2 = SiteFactory(name="456", id=2)

    response = client.get("/sites")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == site1.id
    assert data[0]["name"] == site1.name
    assert data[1]["id"] == site2.id
    assert data[1]["name"] == site2.name


def test_GET_sites_detail_returns_site_based_on_id(client):
    site = SiteFactory(name="123", id=1)

    response = client.get(f"/sites/{site.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == site.id
    assert data["name"] == site.name


def test_GET_sites_detail_returns_error_mesage_if_no_match(client):
    response = client.get(f"/sites/10")
    data = response.get_json()

    assert response.status_code == 404
    assert data["message"] == "Item not found"
