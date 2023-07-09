from typing import Type
from unittest.mock import MagicMock

import pytest

from omnicite.source_factories.main_factory import MainFactory
from omnicite.sources.articles.crossref import Crossref
from omnicite.sources.base_source import BaseSource
from omnicite.sources.books.isbnlib import ISBNLib
from omnicite.sources.websites.new_york_times import NewYorkTimes
from omnicite.sources.websites.substack import Substack
from omnicite.sources.websites.the_guardian import TheGuardian


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
        ("10.1590/0102-311x00133115", Crossref),
        ("https://doi.org/10.1177/21582440231178261", Crossref),
        ("https://www.nytimes.com/2023/05/18/us/tiktok-ban-montana-reaction.html", NewYorkTimes),
        ("9780261102378", ISBNLib),
        (
            "https://www.theguardian.com/australia-news/2023/jul/09/kathryn-campbell-retaining-aukus-role-would-be-"
            "insult-to-robodebt-victims-crossbenchers-say",
            TheGuardian,
        ),
        ("https://www.erininthemorning.com/p/top-5-states-to-be-transgender-in", Substack),
        ("https://heathercoxrichardson.substack.com/p/july-6-2023", Substack),
        (
            "https://fighttorepair.substack.com/p/from-farms-to-pharmaceuticals-its?utm_source=profile"
            "&utm_medium=reader2",
            Substack,
        ),
    ),
)
def test_pull_lever(test_identifier: str, expected_type: Type[BaseSource]):
    result = MainFactory.pull_lever(test_identifier, MagicMock())
    assert result == expected_type
