from typing import Type

import pytest

from omnicite.source_factories.main_factory import MainFactory
from omnicite.sources.articles.raw_doi import RawDOI
from omnicite.sources.base_source import BaseSource
from omnicite.sources.books.raw_isbn import RawISBN
from omnicite.sources.websites.new_york_times_website import NewYorkTimesWebsite


@pytest.mark.parametrize(
    ("test_identifier", "expected"),
    (
        ("https://example.com", True),
        ("http://example.com", True),
        ("example.com/example/page.html", True),
        ("draw.io", True),
        ("test", False),
        ("10.1.1.1", True),
        ("10.1590/0102-311x00133115", False),
        ("https://doi.org/10.1177/21582440231178261", True),
    ),
)
def test_is_url(test_identifier: str, expected: bool):
    result = MainFactory.is_url(test_identifier)
    assert result == expected


@pytest.mark.parametrize(
    ("test_identifier", "expected"),
    (
        ("10.1590/0102-311x00133115", True),
        ("10.1.1.1", False),
        ("https://doi.org/10.1177/21582440231178261", True),
    ),
)
def test_is_doi(test_identifier: str, expected: bool):
    result = MainFactory.is_doi(test_identifier)
    assert result == expected


@pytest.mark.parametrize(
    ("test_identifier", "expected_type"),
    (
        ("10.1590/0102-311x00133115", RawDOI),
        ("https://doi.org/10.1177/21582440231178261", RawDOI),
        ("https://www.nytimes.com/2023/05/18/us/tiktok-ban-montana-reaction.html", NewYorkTimesWebsite),
        ("9780261102378", RawISBN),
    ),
)
def test_pull_lever(test_identifier: str, expected_type: Type[BaseSource]):
    result = MainFactory.pull_lever(test_identifier)
    assert result == expected_type
