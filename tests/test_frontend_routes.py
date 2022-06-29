def test_frontend(client):
    response = client.get("/")
    assert response.status_code == 501
