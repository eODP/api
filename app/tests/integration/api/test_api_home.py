def test_GET_api_home_exists(client):
    response = client.get("/api/")
    data = response.get_json()

    assert response.status_code == 200
    assert data["description"] == "eODP REST API guide"
