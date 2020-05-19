from tests.factories import SectionFactory


def test_GET_sections_works_with_no_section(client):
    response = client.get("/sections")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 0


def test_GET_sections_returns_saved_section(client):
    section1 = SectionFactory(name="123", id=1)
    section2 = SectionFactory(name="456", id=2)

    response = client.get("/sections")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == section1.id
    assert data[0]["name"] == section1.name
    assert data[1]["id"] == section2.id
    assert data[1]["name"] == section2.name


def test_GET_sections_detail_returns_section_based_on_id(client):
    section = SectionFactory(name="123", id=1)

    response = client.get(f"/sections/{section.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == section.id
    assert data["name"] == section.name


def test_GET_sections_detail_returns_error_mesage_if_no_match(client):
    response = client.get(f"/sections/10")
    data = response.get_json()

    assert response.status_code == 404
    assert data["message"] == "Item not found"
