from datetime import date, datetime
from typing import Optional, Tuple

from omnicite.exceptions import OmniCiteSourceFieldError
from omnicite.special_fields.base_special_field import BaseSpecialField


class DateField(BaseSpecialField):
    """Constructs a date and stores and uses it as needed, for dates"""

    def __init__(self, field_contents: date | Tuple[str, str]):
        super().__init__(field_contents)

    @property
    def year(self) -> int:
        return self.field_contents.year

    @staticmethod
    def _convert_time_string_to_date(time_string: str, format_string: Optional[str]) -> date:
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

    def _construct_field(self) -> date:
        if isinstance(self.raw_field_contents, date):
            return self.raw_field_contents
        elif isinstance(self.raw_field_contents, tuple):
            dt = DateField._convert_time_string_to_date(self.raw_field_contents[0], self.raw_field_contents[1])
            return dt

    def __str__(self) -> str:
        out = self.field_contents.isoformat()
        return out
