import pytest

from omnicite.formatters.bibtex_formatter import BibtexFormatter


@pytest.mark.parametrize(
    ("test_string", "expected"),
    (
        ("", ""),
        ("test", "test"),
        ("10% test", r"10\% test"),
        ("10\\% test", r"10\% test"),
        ("test & test", r"test \& test"),
    ),
)
def test_fix_up_string(test_string: str, expected: str):
    result = BibtexFormatter.fix_up_string(test_string)
    assert result == expected


@pytest.mark.parametrize(
    ("test_field_key", "test_field", "expected"),
    (
        ("", "", " = {}"),
        ("test_field", "example of a field", "test_field = {example of a field}"),
    ),
)
def test_convert_field_to_line(test_field_key: str, test_field: str, expected: str):
    result = BibtexFormatter.convert_field_to_line(test_field_key, test_field)
    assert result == expected
