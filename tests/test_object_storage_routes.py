import json

import pytest


@pytest.fixture(autouse=True)
def _mock_paths(tmp_path, monkeypatch):
    import marketplace_standard_app_api.database
    import marketplace_standard_app_api.routers.object_storage

    db_path = tmp_path / "test.db"
    monkeypatch.setattr(
        marketplace_standard_app_api.database,
        "DATABASE_URL",
        f"sqlite:///{db_path.resolve()}",
    )
    monkeypatch.setattr(
        marketplace_standard_app_api.routers.object_storage,
        "DATA_DIR",
        tmp_path / "data",
    )


@pytest.fixture
def collection(client):
    # Create collection
    response = client.put("/data/", headers={"X-Object-Meta-foo": "bar"})
    assert response.ok
    assert response.status_code == 201
    collection_name = response.content.decode("utf-8")

    # Yield collection name
    yield collection_name

    # Delete all datasets.
    response = client.get(f"/data/{collection_name}")
    if response.status_code == 200:
        for dataset in response.json():
            client.delete(f"/data/{collection_name}/{dataset['name']}")
    # Delete collection
    assert client.delete(f"/data/{collection_name}").status_code == 204
    # Check that collection is deleted
    assert client.head(f"/data/{collection_name}").status_code == 404


def test_insert_collection_with_metadata(client):
    response = client.get("/data")
    assert response.ok
    assert response.status_code == 204

    response = client.put("/data/", headers={"X-Object-Meta-foo": "bar"})
    assert response.ok
    assert response.status_code == 201
    collection_id = response.content.decode("utf-8")

    response = client.head(f"/data/{collection_id}")
    assert response.ok
    assert response.status_code == 204
    assert "X-Object-Meta-foo".lower() in (
        key.lower() for key in response.headers.keys()
    )

    response = client.get("/data")
    assert response.ok
    assert response.status_code == 200
    collections = response.json()
    assert len(collections) == 1


def test_create_and_delete_json_dataset(client, collection, tmp_path):
    p = tmp_path / "test.json"
    p.write_text(json.dumps({"foo": "bar"}))

    assert client.get(f"/data/{collection}").status_code == 204
    assert client.head(f"/data/{collection}/test.json").status_code == 404
    assert client.get(f"/data/{collection}/test.json").status_code == 404

    assert (
        client.put(
            f"data/{collection}/test.json",
            files={"file": ("test.json", p.open("rb"), "application/json")},
        ).status_code
        == 201
    )

    assert client.head(f"/data/{collection}").status_code == 204
    assert client.get(f"/data/{collection}").status_code == 200

    response = client.head(f"/data/{collection}/test.json")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "last-modified" in response.headers.keys()

    response = client.get(f"/data/{collection}/test.json")
    assert response.status_code == 200
    assert response.json() == {"foo": "bar"}
    assert response.headers["Content-Type"] == "application/json"
    assert "last-modified" in response.headers.keys()

    assert client.delete(f"/data/{collection}").status_code == 409
    assert client.delete(f"/data/{collection}/test.json").status_code == 204
    assert client.head(f"/data/{collection}/test.json").status_code == 404
    assert client.get(f"/data/{collection}/test.json").status_code == 404
    assert client.get(f"/data/{collection}").status_code == 204
