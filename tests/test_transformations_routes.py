from time import sleep
from uuid import UUID

import pytest

from marketplace_standard_app_api.models.transformation import TransformationModel


@pytest.fixture(autouse=True)
def _mock_paths(monkeypatch, tmp_path):
    import marketplace_standard_app_api.reference.simulation_controller.simulation

    monkeypatch.setattr(
        marketplace_standard_app_api.reference.simulation_controller.simulation,
        "SIMULATIONS_FOLDER_PATH",
        tmp_path / "simulations",
    )


def test_access_non_existing_transformation(client):
    non_existent_transformation_id = UUID("63ed5190-82cb-4f02-88ce-5644faf6d876")
    response = client.get(f"/transformations/{non_existent_transformation_id}")
    assert response.status_code == 404
    assert not response.ok


def test_transformation_lifecycle(client):
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
