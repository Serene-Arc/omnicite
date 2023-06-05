import pytest

from omnicite.special_fields.name import Name


@pytest.mark.parametrize(
    ("test_raw_name", "expected"),
    (
        ("John Doe", "John Doe"),
        ("john doe", "John Doe"),
        ("CS Lewis", "C. S. Lewis"),
        ("CS lewis", "C. S. Lewis"),
        ("C.S. Lewis", "C. S. Lewis"),
        ("John Doe, Jr.", "John Doe Jr."),
        ("{Federal Government of Australia}", "Federal Government of Australia"),
        ("Guillermo de la Cruz", "Guillermo de la Cruz"),
        ("Guillermo del Toro", "Guillermo del Toro"),
        ("Johann Wolfgang von Goethe", "Johann Wolfgang von Goethe"),
        ("johann wolfgang von goethe", "Johann Wolfgang von Goethe"),
        ("Chigozie Nelson Nkalu", "Chigozie Nelson Nkalu"),
    ),
)
def test_format_to_string(test_raw_name: str, expected: str):
    test_name = Name(test_raw_name)
    assert str(test_name) == expected
