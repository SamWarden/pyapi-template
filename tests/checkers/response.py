from pprint import pformat

import httpx


def assert_response(
    response: httpx.Response,
    status_code: int,
    data: dict[object, object] | list[object] | None = None,
) -> None:
    """
    Asserts that the response has the expected status code and data.

    :param response: The HTTP response to check.
    :param status_code: The expected HTTP status code.
    :param data: The expected response data.
    """
    url_path = response.url.path
    assert response.status_code == status_code, (
        f"{url_path}: Expected status code {status_code}, "
        f"but got {response.status_code}. Response data: {pformat(response.json())}"
    )

    assert response.json() == data, (
        f"{url_path}: Wrong response data.\n"
        f"Expected response data \n{pformat(data)},\n"
        f"but got\n{pformat(response.json())}\n"
        f"Difference:\n{pformat(find_differences(actual=response.json(), expected=data))}"
    )


def find_differences(actual: object, expected: object, path: str = "") -> list[str]:
    differences = []

    if isinstance(actual, dict) and isinstance(expected, dict):
        actual_keys = set(actual.keys())
        expected_keys = set(expected.keys())

        for key in actual_keys.union(expected_keys):
            new_path = f"{path}.{key}" if path else key

            if key not in actual:
                differences.append(f"Missing key in actual: {new_path}")
            elif key not in expected:
                differences.append(f"Extra key in actual: {new_path}")
            else:
                differences += find_differences(actual[key], expected[key], new_path)

    elif isinstance(actual, list) and isinstance(expected, list):
        min_len = min(len(actual), len(expected))
        for index in range(min_len):
            new_path = f"{path}[{index}]"
            differences += find_differences(actual[index], expected[index], new_path)

        if len(actual) > len(expected):
            for index in range(len(expected), len(actual)):
                differences.append(f"Extra item at {path}[{index}]: {actual[index]}")
        elif len(expected) > len(actual):
            for index in range(len(actual), len(expected)):
                differences.append(f"Missing item at {path}[{index}]: {expected[index]}")
    elif actual != expected:
        differences.append(f"Value mismatch at {path}: actual={actual!r}, expected={expected!r}")

    return differences
