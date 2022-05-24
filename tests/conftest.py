#!/usr/bin/env python

""".. currentmodule:: conftest.

.. moduleauthor:: Carl Simon Adorf <simon.adorf@epfl.ch>

Provide fixtures for all tests.
"""

import json
from pathlib import Path

import pytest

from marketplace_standard_app_api import api


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
