from typing import Optional, Tuple

import pytest

import omnicite.__main__ as main


@pytest.mark.parametrize(
    ("test_string", "expected"),
    (
        ("", (None, "")),
        ("test", (None, "test")),
        ("blah:test", (None, "blah:test")),
        ("blah:::test", ("blah", "test")),
        (":::test", (None, "test")),
    ),
)
def test_separate_module_name(test_string: str, expected: tuple[Optional[str], str]):
    result = main.separate_specified_module(test_string)
    assert result == expected
