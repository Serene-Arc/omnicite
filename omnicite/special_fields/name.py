import re
from typing import Sequence

import regex


class Name:
    family_name_words = (
        "bin",
        "de",
        "del",
        "den",
        "ibn",
        "la",
        "van",
        "von",
    )
    family_name_hyphenated_prefixes = ("al",)
    name_qualifications = (
        "PhD",
        "MD",
    )
    formal_name_suffixes = ("Jr",)

    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.person_name: bool = True
        self._first_name: list[str] = []
        self._family_name: list[str] = []
        self.middle_name_parts: list[str] = []
        self.name_suffixes: list[str] = []
        self.name_qualifications: list[str] = []

        self._separate_out_name_parts()
        self._format_name()

    @property
    def family_name(self) -> str:
        return " ".join(self._family_name)

    @property
    def final_name(self) -> str:
        return self._family_name[-1]

    def _name_pre_processing(self, name_string: str) -> list[str]:
        if name_string.startswith("{"):
            self.person_name = False
            return [
                name_string.strip("{}"),
            ]
        self.person_name = True
        single_string_formatting_functions = (Name._strip_characters,)
        for func in single_string_formatting_functions:
            name_string = func(name_string)

        out = re.split(" ", name_string)
        return out

    def _format_name(self):
        separate_string_formatting_functions = (
            (
                Name._separate_initials,
                (
                    "_first_name",
                    "middle_name_parts",
                ),
            ),
            (
                Name._capitalise_name_parts_first_letter,
                (
                    "_first_name",
                    "middle_name_parts",
                    "_family_name",
                ),
            ),
            (
                Name._capitalise_roman_numerals,
                ("name_suffixes",),
            ),
        )
        for func, variables in separate_string_formatting_functions:
            for variable in variables:
                self.__dict__[variable] = func(self.__dict__[variable])

    @staticmethod
    def _capitalise_roman_numerals(in_strings: Sequence[str]) -> Sequence[str]:
        out = [s.upper() if Name.is_roman_numeral(s) else s for s in in_strings]
        return out

    @staticmethod
    def _capitalise_name_parts_first_letter(in_strings: Sequence[str]) -> Sequence[str]:
        out = []
        for s in in_strings:
            if s not in Name.family_name_words and s[0].islower():
                if "-" in s:
                    sub_parts = re.split(r"-", s)
                    temp = []
                    for part in sub_parts:
                        if part in Name.family_name_hyphenated_prefixes:
                            temp.append(part)
                        else:
                            temp.append(part[0].upper() + part[1:])
                    out.append("-".join(temp))
                else:
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
        initial_pattern = regex.compile(r"([A-Z]\.?(?!\p{Ll}+)|[a-z]\.)")
        for s in in_strings:
            matches = initial_pattern.findall(s)
            if matches:
                for group in matches:
                    out.append(group.strip(" .") + ".")
            elif len(s) == 1 and s.isupper():
                out.append(s + ".")
            elif all(c.isupper() for c in s):
                out.extend([c + "." for c in s])
            else:
                out.append(s)
        return out

    def _separate_out_name_parts(self):
        parts = self._name_pre_processing(self.raw_text)

        self.name_qualifications = [p for p in parts if p in self.name_qualifications]
        parts = [p for p in parts if p not in self.name_qualifications]

        max_i = -1
        for i, p in enumerate(reversed(parts), start=1):
            if p in self.formal_name_suffixes or self.is_roman_numeral(p):
                self.name_suffixes.append(p)
                max_i = i
            else:
                break
        if self.name_suffixes:
            self.name_suffixes.reverse()
            parts = parts[:-max_i]

        max_i = -1
        for i, p in enumerate(reversed(parts[:-1]), start=2):
            if p in self.family_name_words:
                self._family_name.append(p)
                max_i = i
            else:
                break
        self._family_name.insert(0, parts[-1])
        if max_i >= 0:
            self._family_name.reverse()
            parts = parts[:-max_i]
        else:
            parts = parts[:-1]

        if len(parts) > 1:
            self.middle_name_parts = parts[1:]
            parts = parts[:1]
        self._first_name = parts

    @staticmethod
    def is_roman_numeral(in_string: str) -> bool:
        in_string = in_string.upper()
        pattern = re.compile(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")
        if pattern.match(in_string):
            return True
        else:
            return False

    def __str__(self):
        out = " ".join(
            self._first_name
            + self.middle_name_parts
            + self._family_name
            + self.name_suffixes
            + self.name_qualifications
        )
        return out
