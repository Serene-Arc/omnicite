from typing import Sequence, Type, Union
from unittest.mock import MagicMock

import pytest

import omnicite.exceptions as omnicite_exceptions
from omnicite.sources.base_source import BaseSource


@pytest.mark.parametrize(
    ("test_required_fields", "test_key_fields"),
    (
        (
            (
                "test",
                (
                    "test1",
                    "test2",
                ),
            ),
            ("test1",),
        ),
    ),
)
def test_check_field_existence_and_exclusivity(
    test_required_fields: Sequence[Union[str, Sequence[str]]],
    test_key_fields: Sequence[str],
):
    BaseSource.check_field_existence_and_exclusivity(test_required_fields, test_key_fields)


@pytest.mark.parametrize(
    ("test_required_fields", "test_key_fields", "exception_string"),
    (
        (
            (
                "test",
                (
                    "test1",
                    "test2",
                ),
            ),
            (),
            "No field found",
        ),
        (
            (
                "test",
                (
                    "test1",
                    "test2",
                ),
            ),
            ("test",),
            "No field found",
        ),
        (
            (
                "test",
                (
                    "test1",
                    "test2",
                ),
            ),
            (
                "test",
                "test1",
                "test2",
            ),
            "Multiple exclusive fields",
        ),
    ),
)
def test_check_field_existence_and_exclusivity(
    test_required_fields: Sequence[Union[str, Sequence[str]]],
    test_key_fields: Sequence[str],
    exception_string: str,
):
    with pytest.raises(omnicite_exceptions.OmniCiteSourceFieldError) as excinfo:
        BaseSource.check_field_existence_and_exclusivity(test_required_fields, test_key_fields)
    assert exception_string in str(excinfo.value)


@pytest.mark.parametrize(
    ("test_required_fields", "test_key_fields", "expected"),
    (
        ((), (), ()),
        (
            ("test1",),
            ("test1",),
            ("test1",),
        ),
        (
            (
                "test1",
                ("test2", "test3"),
            ),
            (
                "test1",
                "test3",
            ),
            ("test1", "test3"),
        ),
        (
            (
                "test1",
                ("test2", "test3"),
            ),
            (
                "test3",
                "test1",
            ),
            ("test1", "test3"),
        ),
    ),
)
def test_get_all_filled_required_fields(
    test_required_fields: Sequence[Union[str, Sequence[str]]],
    test_key_fields: Sequence[str],
    expected: Sequence[str],
):
    result = BaseSource.get_all_filled_required_fields(test_required_fields, test_key_fields)
    assert len(result) == len(expected)
    assert all([r == expected[i] for i, r in enumerate(result)])


@pytest.mark.parametrize(
    (
        "test_optional_fields",
        "test_key_fields",
        "expected",
    ),
    (
        ((), (), ()),
        (
            (
                "option1",
                "option2",
            ),
            (
                "option1",
                "option2",
            ),
            (
                "option1",
                "option2",
            ),
        ),
        (
            (
                "option1",
                "option2",
            ),
            (
                "option2",
                "option1",
            ),
            (
                "option1",
                "option2",
            ),
        ),
        (
            (
                "option1",
                "option2",
                ("subopt1", "subopt2"),
            ),
            (
                "option2",
                "subopt2",
                "option1",
            ),
            ("option1", "option2", "subopt2"),
        ),
    ),
)
def test_get_all_filled_optional_fields(
    test_optional_fields: Sequence[Union[str, Sequence[str]]],
    test_key_fields: Sequence[str],
    expected: Sequence[str],
):
    result = BaseSource.get_all_filled_optional_fields(test_optional_fields, test_key_fields)
    assert len(result) == len(expected)
    assert all([r == expected[i] for i, r in enumerate(result)])
