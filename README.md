# README

## About

This repository contains the specification of the Materials MarketPlace Standard App API.
The API is used as basis for the interaction between apps on the Materials MarketPlace platform.

This repository contains the API version: 0.5.0.

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

You can install this package from PyPI with:
```console
pip install marketplace-standard-app-api
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

## For maintainers

To create a new release, clone the repository, install development dependencies with `pip install -e '.[dev]'`, and then execute `bumpver update --[major|minor|patch]`.
This will:

  1. Create a tagged release with bumped version and push it to the repository.
  2. Trigger a GitHub actions workflow that creates a GitHub release and publishes it on PyPI.

Additional notes:

  - The project follows semantic versioning.
  - Use the `--dry` option to preview the release change.

## Acknowledgements

This work is supported by the MarketPlace project funded by [Horizon 2020](https://ec.europa.eu/programmes/horizon2020/) under the H2020-NMBP-25-2017 call (Grant No. 760173).
