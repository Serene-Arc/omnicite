from typing import Sequence

from omnicite.exceptions import OmniCiteSourceFieldError
from omnicite.special_fields.base_special_field import BaseSpecialField
from omnicite.special_fields.name import Name


class NameField(BaseSpecialField):
    def __init__(self, field_contents: Sequence[Name]):
        if not field_contents:
            raise OmniCiteSourceFieldError(f"Name field requires a name; field was initialised with '{field_contents}'")
        super().__init__(field_contents)

    def __str__(self) -> str:
        out = " and ".join([str(f) for f in self.field_contents])
        return out

    @staticmethod
    def construct_name_field(in_strings: str | Sequence[str]) -> "NameField":
        if isinstance(in_strings, str):
            in_strings = [
                in_strings,
            ]
        names = [Name(s) for s in in_strings]
        out = NameField(names)
        return out
