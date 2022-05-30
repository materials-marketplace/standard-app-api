def test_marketplace_openapi_specification_is_present(
    marketplace_openapi_specification_file_path,
):
    return marketplace_openapi_specification_file_path.exists()


def test_marketplace_openapi_specification_file_in_sync(
    marketplace_openapi_specification_file,
    marketplace_openapi,
):
    assert marketplace_openapi_specification_file == marketplace_openapi
