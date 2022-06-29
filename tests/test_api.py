import json
from time import sleep
from uuid import UUID

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

import marketplace_standard_app_api.database
import marketplace_standard_app_api.routers.object_storage
from marketplace_standard_app_api import api
from marketplace_standard_app_api.main import auth_token_bearer
from marketplace_standard_app_api.models.transformation import TransformationModel


async def _fake_auth_token_bearer(request: Request):
    return None


@pytest.fixture
def client(tmp_path, monkeypatch):
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

    api.dependency_overrides[auth_token_bearer] = _fake_auth_token_bearer
    client = TestClient(api)
    with client:
        yield client
    api.dependency_overrides = {}


@pytest.fixture(autouse=True)
def _mock_simulation_dir(monkeypatch, tmp_path):
    import marketplace_standard_app_api.reference.simulation_controller.simulation

    monkeypatch.setattr(
        marketplace_standard_app_api.reference.simulation_controller.simulation,
        "SIMULATIONS_FOLDER_PATH",
        tmp_path / "simulations",
    )


def test_frontend(client):
    response = client.get("/")
    assert response.status_code == 501


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


def test_access_non_existing_transformation(client):
    non_existent_transformation_id = UUID("63ed5190-82cb-4f02-88ce-5644faf6d876")
    response = client.get(f"/transformations/{non_existent_transformation_id}")
    assert response.status_code == 404
    assert not response.ok


def test_create_and_runtransformation(client):
    response = client.get("transformations")
    assert len(response.json()["items"]) == 0
    assert response.status_code == 200
    assert response.ok

    response = client.post("/transformations", json={"parameters": {"input_value": 10}})
    assert response.status_code == 200
    transformation_id = response.json()["id"]

    response = client.get("transformations")
    assert len(response.json()["items"]) == 1
    transformation = TransformationModel(**response.json()["items"][0])
    assert str(transformation.id) == transformation_id
    assert response.status_code == 200
    assert response.ok

    response = client.get(f"/transformations/{transformation_id}")
    assert response.json()["id"] == transformation_id
    assert response.json()["state"] == "CREATED"
    assert response.ok

    response = client.get(f"/transformations/{transformation_id}/state")
    assert response.json()["id"] == transformation_id
    assert response.json()["state"] == "CREATED"

    response = client.patch(
        f"/transformations/{transformation_id}", json={"state": "CREATED"}
    )
    assert response.status_code == 422

    response = client.patch(
        f"/transformations/{transformation_id}", json={"state": "STOPPED"}
    )
    assert response.status_code == 409

    response = client.patch(
        f"/transformations/{transformation_id}", json={"state": "RUNNING"}
    )
    assert response.ok
    assert response.json()["id"] == transformation_id
    assert response.json()["state"] == "RUNNING"

    sleep(3)

    response = client.get(f"/transformations/{transformation_id}")
    assert response.ok
    assert response.json()["id"] == transformation_id
    assert response.json()["state"] == "COMPLETED"

    response = client.delete(f"/transformations/{transformation_id}")
    assert response.status_code == 204
    assert response.ok

    response = client.get(f"/transformations/{transformation_id}")
    assert response.status_code == 404
    assert not response.ok
