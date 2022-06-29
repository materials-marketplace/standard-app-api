#!/usr/bin/env python

""".. currentmodule:: conftest.

.. moduleauthor:: Carl Simon Adorf <simon.adorf@epfl.ch>

Provide fixtures for all tests.
"""

import json
from pathlib import Path

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from marketplace_standard_app_api import api
from marketplace_standard_app_api.main import auth_token_bearer


@pytest.fixture
def marketplace_openapi_specification_file_path():
    return Path("openapi.json")


@pytest.fixture
def marketplace_openapi_specification_file():
    return json.loads(Path("openapi.json").read_text())


@pytest.fixture
def marketplace_api():
    return api


@pytest.fixture
def marketplace_openapi():
    return api.openapi()


async def _fake_auth_token_bearer(request: Request):
    return None


@pytest.fixture
def client():
    api.dependency_overrides[auth_token_bearer] = _fake_auth_token_bearer

    client = TestClient(api)
    with client:
        yield client
    api.dependency_overrides = {}
