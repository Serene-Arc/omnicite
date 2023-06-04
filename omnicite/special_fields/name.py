import re
from typing import Sequence


class Name:
    def __init__(self, raw_text: str):
        self.person_name = None
        self.name_strings = self.format_name(raw_text)

    def format_name(self, name_string: str) -> Sequence[str]:
        if name_string.startswith("{"):
            self.person_name = False
            return [
                name_string.strip("{}"),
            ]
        self.person_name = True
        single_string_formatting_functions = (Name._strip_characters,)
        for func in single_string_formatting_functions:
            name_string = func(name_string)

        out = Name._separate_name_parts(name_string)

        separate_string_formatting_functions = (
            Name._separate_initials,
            Name._capitalise_name_parts,
        )
        for func in separate_string_formatting_functions:
            out = func(out)

        return out

    @staticmethod
    def _capitalise_name_parts(in_strings: Sequence[str]) -> Sequence[str]:
        exception_words = (
            "de",
            "la",
            "van",
            "von",
        )
        out = []
        for s in in_strings:
            if s not in exception_words and s[0].islower():
                out.append(s[0].upper() + s[1:] if len(s) > 1 else s[0].upper())
            else:
                out.append(s)
        return out

    @staticmethod
    def _strip_characters(in_string: str) -> str:
        out = in_string.replace(",", "")
        return out

    @staticmethod
    def _separate_initials(in_strings: Sequence[str]) -> Sequence[str]:
        out = []
        initial_pattern = re.compile(r"([A-Z])\.?(?![a-z])")
        for s in in_strings:
            matches = initial_pattern.findall(s)
            if matches:
                for group in matches:
                    out.append(group + ".")
            else:
                out.append(s)
        return out

    @staticmethod
    def _separate_name_parts(in_string: str) -> Sequence[str]:
        out = re.split(r" ", in_string)
        return out

    def __str__(self):
        return " ".join(self.name_strings)
