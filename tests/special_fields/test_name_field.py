from typing import Sequence

import pytest

from omnicite.special_fields.name_field import NameField


@pytest.mark.parametrize(
    ("test_names", "expected"),
    (
        ("John Smith", "John Smith"),
        (["John Smith", "Jane Doe"], "John Smith and Jane Doe"),
    ),
)
def test_convert_to_text(test_names: str | Sequence[str], expected: str):
    test_name_field = NameField(test_names)
    result = str(test_name_field)
    assert result == expected
