import re

from omnicite.formatters.base_formatter import BaseFormatter
from omnicite.sources.base_source import BaseSource
from omnicite.special_fields.base_special_field import BaseSpecialField


class BibtexFormatter(BaseFormatter):
    @staticmethod
    def convert_source(source: BaseSource) -> str:
        out = [
            f"@{source.entry_type}{{{source.identifier},",
        ]
        for field in source.fields.keys():
            out.append(f"{field} = {{{source.fields[field]}}},")
        out.append("}")
        return "\n".join(out)

    @staticmethod
    def convert_field_to_line(field_key: str, field: str | BaseSpecialField) -> str:
        field = BibtexFormatter.fix_up_string(field)
        out = f"{field_key} = {{{str(field)}}}"
        return out

    @staticmethod
    def fix_up_string(in_string: str) -> str:
        in_string = re.sub(r"(?<!\\)%", r"\%", in_string)
        in_string = re.sub(r"(?<!\\)&", r"\&", in_string)
        return in_string
