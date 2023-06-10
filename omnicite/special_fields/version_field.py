import re

from omnicite.exceptions import OmniCiteSourceFieldError
from omnicite.special_fields.base_special_field import BaseSpecialField


class VersionField(BaseSpecialField):
    def __init__(self, field_contents: str):
        super().__init__(field_contents)

    def __str__(self) -> str:
        return f"v{self.field_contents}"

    def _construct_field(self):
        pattern = re.compile(r"(\d+)\.(\d+)\.(\d+)")
        matches = pattern.search(self.raw_field_contents)
        if matches:
            return ".".join(matches.groups())
        raise OmniCiteSourceFieldError(f"Could not create version field from string {self.raw_field_contents}")
