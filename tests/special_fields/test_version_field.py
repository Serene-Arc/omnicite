import pytest

from omnicite.special_fields.version_field import VersionField


@pytest.mark.parametrize(
    ("test_string", "expected"),
    (
        ("0.0.1", "v0.0.1"),
        ("v0.0.1", "v0.0.1"),
    ),
)
def test_make_field(test_string: str, expected: str):
    test_field = VersionField(test_string)
    assert str(test_field) == expected
