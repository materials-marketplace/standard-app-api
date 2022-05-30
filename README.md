# README

## About

This repository contains the specification of the Materials MarketPlace Standard App API.
The API is used as basis for the interaction between apps on the Materials MarketPlace platform.

This repository contains the API version: 0.1.0.

## Authors

- Simon Adorf (simon.adorf@epfl.ch)
- MarketPlace consortium partners

## Specification

The repository contains both a programmatic definition of the API (implemented via [Pydantic](https://pydantic-docs.helpmanual.io/) and [FastAPI](https://fastapi.tiangolo.com/)) within the [marketplace_standard_app_api.main](marketplace_standard_app_api/__main__.py) module as well as an equivalent [OpenAPI](https://www.openapis.org/) representation in the [openapi.json](openapi.json) file.
Programmatic checks are performed to ensure that both representations remain synchronized and conflict-free.
In case that the definition within the Python module and the OpenAPI JSON-file are conflicting with each other for whatever reason, the former must be considered authoritive.

Tip: You can use the `marketplace-standard-app-api show` command to generate the OpenAPI file from the Python module (requires the `cli` extra).

## Installation

Note: Users should use the [MarketPlace Python SDK](https://github.com/materials-marketplace/python-sdk) for app development.

You can install this package from source with:
```console
pip install git+https://github.com/materials-marketplace/standard-app-api
```

To install extras, first clone the repository, e.g.,:
```console
git clone https://github.com/materials-marketplace/standard-app-api
cd standard-app-api/
pip install '.[cli]'
```

## Tests

Tests for this repository are implemented via [pytest](https://pytest.org/).
To run these tests, first install the test dependencies with
```console
pip install '.[tests]'
```
and then run the tests with the `pytest` command.

## Contributing

Contributions in the form of issues, comments, and pull request are very welcome.

To make code contributions, please fork this repository, and then create a pull request.
For development you will need to setup a Python environment (with a recent Python version), install the development requiremments, and the pre-commit hooks with:
```console
pip install pre-commit==2.17.0
pre-commit install
```

## Acknowledgements

This work is supported by the MarketPlace project funded by [Horizon 2020](https://ec.europa.eu/programmes/horizon2020/) under the H2020-NMBP-25-2017 call (Grant No. 760173).
