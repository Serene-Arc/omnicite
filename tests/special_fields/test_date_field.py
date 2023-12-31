import datetime

import pytest

from omnicite.exceptions import OmniCiteSourceFieldError
from omnicite.special_fields.date_field import DateField


@pytest.mark.parametrize(
    ("test_time_string", "test_format_string", "expected"),
    (
        ("1/6/2023", "%d/%m/%Y", datetime.date(2023, 6, 1)),
        ("1/6/2023", "%m/%d/%Y", datetime.date(2023, 1, 6)),
        ("1/6/23", "%d/%m/%y", datetime.date(2023, 6, 1)),
        ("2016-12-07T21:52:08Z", None, datetime.date(2016, 12, 7)),
    ),
)
def test_convert_time_string_to_datetime(test_time_string: str, test_format_string: str, expected: datetime.datetime):
    result = DateField._convert_time_string_to_date(test_time_string, test_format_string)
    assert result == expected


@pytest.mark.parametrize(
    ("test_time_string", "test_format_string"),
    (("1/6/23", "%d/%m/%Y"),),
)
def test_convert_time_string_to_datetime_exception(test_time_string: str, test_format_string: str):
    with pytest.raises(OmniCiteSourceFieldError):
        DateField._convert_time_string_to_date(test_time_string, test_format_string)
