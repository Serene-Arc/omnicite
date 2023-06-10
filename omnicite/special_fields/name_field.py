from typing import Sequence

from omnicite.exceptions import OmniCiteSourceFieldError
from omnicite.special_fields.base_special_field import BaseSpecialField
from omnicite.special_fields.name import Name


class NameField(BaseSpecialField):
    def __init__(self, field_contents: str | Sequence[Name | str]):
        if not field_contents:
            raise OmniCiteSourceFieldError(f"Name field requires a name; field was initialised with '{field_contents}'")
        super().__init__(field_contents)

    def __str__(self) -> str:
        out = " and ".join([str(f) for f in self.field_contents])
        return out

    def _construct_field(self) -> Sequence[Name]:
        if isinstance(self.raw_field_contents, str):
            self.raw_field_contents = [
                self.raw_field_contents,
            ]
        names = [Name(s) if isinstance(s, str) else s for s in self.raw_field_contents]
        return names
