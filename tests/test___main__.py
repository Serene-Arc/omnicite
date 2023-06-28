from typing import Optional

import pytest

import omnicite.__main__ as main


@pytest.mark.parametrize(
    ("test_string", "expected"),
    (
        ("", None),
        ("test", None),
        ("blah:test", None),
        ("blah:::test", "blah"),
    ),
)
def test_separate_module_name(test_string: str, expected: Optional[str]):
    result = main.separate_specified_module(test_string)
    assert result == expected
