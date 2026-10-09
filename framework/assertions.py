"""Domain-specific assertions for payment testing."""
import json

def assert_status(response, expected_code):
    assert response.status_code == expected_code, (
        f"Expected {expected_code}, got {response.status_code}: {response.text[:200]}"
    )

def assert_json_field(response, field, expected=None):
    data = response.json()
    assert field in data, f"Missing field '{field}' in response"
    if expected is not None:
        assert data[field] == expected, f"Field '{field}': expected {expected}, got {data[field]}"

def assert_response_time(response, max_ms):
    assert response.elapsed_ms <= max_ms, (
        f"Response took {response.elapsed_ms:.1f}ms, exceeds {max_ms}ms SLA"
    )

def assert_schema(response, schema):
    """Validate response JSON against a field-type schema dict."""
    data = response.json()
    for field, expected_type in schema.items():
        assert field in data, f"Schema violation: missing '{field}'"
        assert isinstance(data[field], expected_type), (
            f"Schema violation: '{field}' expected {expected_type.__name__}, "
            f"got {type(data[field]).__name__}"
        )
