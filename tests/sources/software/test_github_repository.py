from datetime import date
from typing import Sequence
from unittest.mock import MagicMock

import pytest

from omnicite.sources.software.github_repository import GitHubRepository
from omnicite.special_fields.base_special_field import BaseSpecialField
from omnicite.special_fields.date_field import DateField
from omnicite.special_fields.name_field import NameField
from omnicite.special_fields.version_field import VersionField


@pytest.mark.online
@pytest.mark.parametrize(
    ("test_identifier", "expected_dict"),
    (
        (
            "https://github.com/michadenheijer/pynytimes",
            {
                "author": "Micha den Heijer",
                "title": "pynytimes",
                "url": "https://github.com/michadenheijer/pynytimes",
                "version": "v0.10.0",
                "year": "2023",
            },
        ),
        (
            "https://github.com/aliparlakci/bulk-downloader-for-reddit",
            {
                "author": "Ali Parlakçı",
                "title": "bulk-downloader-for-reddit",
                "url": "https://github.com/aliparlakci/bulk-downloader-for-reddit",
                "date": "2023-01-31",
                "version": "v2.6.2",
            },
        ),
    ),
)
def test_make_source(
    test_identifier: str,
    expected_dict: dict[str, str | BaseSpecialField],
):
    test_source = GitHubRepository(test_identifier)
    assert all([str(test_source.fields[key]) == expected_dict[key] for key in expected_dict.keys()])


@pytest.mark.parametrize(
    ("test_fields", "existing_identifiers", "expected"),
    (
        (
            {
                "author": NameField("Micha den Heijer"),
                "title": "pynytimes",
                "version": VersionField("0.10.0"),
                "date": DateField(date(2023, 4, 21)),
            },
            (),
            "heijer_2023_v0.10.0",
        ),
        (
            {
                "author": NameField("Micha den Heijer"),
                "title": "pynytimes",
                "version": VersionField("0.10.0"),
                "date": DateField(date(2023, 4, 21)),
            },
            ("heijer_2023_v0.10.0",),
            "heijer_2023_v0.10.0_1",
        ),
    ),
)
def test_generate_unique_identifier(
    test_fields: dict[str, str | BaseSpecialField],
    existing_identifiers: Sequence[str],
    expected: str,
):
    class TestGithubRepository(GitHubRepository):
        def __init__(self, identifier: str):
            super().__init__(identifier)
            self.fields = test_fields

        def retrieve_information(self):
            pass

    test_source = TestGithubRepository("test")
    result = test_source.generate_unique_identifier(existing_identifiers)
    assert result == expected
