from app import create_app


def test_home_page():
    client = create_app().test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["status"] == "running"
