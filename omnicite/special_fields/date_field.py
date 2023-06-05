from datetime import date, datetime
from typing import Optional

from omnicite.exceptions import OmniCiteSourceFieldError
from omnicite.special_fields.base_special_field import BaseSpecialField


class DateField(BaseSpecialField):
    """Constructs a datetime and stores and uses it as needed, for dates"""

    def __init__(self, field_contents: date):
        super().__init__(field_contents)

    @staticmethod
    def convert_time_string_to_date(time_string: str, format_string: Optional[str]) -> date:
        try:
            if format_string:
                dt = datetime.strptime(time_string, format_string)
            else:
                dt = datetime.fromisoformat(time_string)
            dt = dt.date()
            return dt
        except ValueError:
            raise OmniCiteSourceFieldError(
                f"The time string '{time_string}' does not match the format string '{format_string}'"
            )

    @staticmethod
    def construct_date_field(time_string: str, format_string: Optional[str] = None) -> "DateField":
        dt = DateField.convert_time_string_to_date(time_string, format_string)
        return dt

    def __str__(self) -> str:
        out = self.field_contents.isoformat()
        return out
