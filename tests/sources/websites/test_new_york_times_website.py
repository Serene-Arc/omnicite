from datetime import date
from typing import Sequence
from unittest.mock import MagicMock, patch

import pytest
from confuse import Configuration

from omnicite.sources.websites.new_york_times_website import NewYorkTimesWebsite
from omnicite.special_fields.base_special_field import BaseSpecialField
from omnicite.special_fields.date_field import DateField
from omnicite.special_fields.name_field import NameField


@pytest.mark.online
@pytest.mark.parametrize(
    ("test_url", "expected_dict"),
    (
        (
            "https://www.nytimes.com/2023/06/04/us/state-legislatures-opposite-agendas.html",
            {
                "author": "Mitch Smith",
                "date": "2023-06-04",
                "organization": "New York Times",
                "subtitle": "With single-party statehouse control at its highest level in decades, legislators"
                " across much of the country leaned into cultural issues and bulldozed the opposition.",
                "title": "In a Contentious Lawmaking Season, Red States Got Redder and Blue Ones Bluer",
                "url": "https://www.nytimes.com/2023/06/04/us/state-legislatures-opposite-agendas.html",
                "urldate": date.today().isoformat(),
            },
        ),
        (
            "https://www.nytimes.com/2023/06/02/us/guam-typhoon-mawar.html",
            {
                "author": "Josie Moyer and Jacey Fortin",
                "date": "2023-06-02",
                "organization": "New York Times",
                "subtitle": "The storm was the strongest to strike the U.S. Pacific territory in at least two decades.",
                "title": "Many in Guam Lack Power and Water a Week After Typhoon Mawar",
                "url": "https://www.nytimes.com/2023/06/02/us/guam-typhoon-mawar.html",
                "urldate": date.today().isoformat(),
            },
        ),
        (
            "https://www.nytimes.com/2023/05/18/us/tiktok-ban-montana-reaction.html",
            {
                "author": "Jacey Fortin and Eliza Fawcett and Jim Robbins",
                "date": "2023-05-18",
                "organization": "New York Times",
                "subtitle": "Users of the popular social media site were less than pleased by the ban, enacted over "
                "fears that sensitive user data could end up in the hands of the Chinese government.",
                "title": "In Montana, a TikTok Ban Could Be a ‘Kick in the Face’",
                "url": "https://www.nytimes.com/2023/05/18/us/tiktok-ban-montana-reaction.html",
                "urldate": date.today().isoformat(),
            },
        ),
    ),
)
def test_make_source(
    test_url: str,
    expected_dict: dict[str, str | BaseSpecialField],
    test_configuration: Configuration,
):
    test_source = NewYorkTimesWebsite(test_url, test_configuration)
    assert all([str(test_source.fields[key]) == expected_dict[key] for key in expected_dict.keys()])


@pytest.mark.parametrize(
    ("test_string", "expected"),
    (
        (
            "BY MITCH SMITH",
            [
                "mitch smith",
            ],
        ),
        (
            "BY JOSIE MOYER AND JACEY FORTIN",
            [
                "josie moyer",
                "jacey fortin",
            ],
        ),
        (
            "BY JACEY FORTIN, ELIZA FAWCETT AND JIM ROBBINS",
            [
                "jacey fortin",
                "eliza fawcett",
                "jim robbins",
            ],
        ),
    ),
)
def test_split_and_sanitise_byline(test_string: str, expected: Sequence[str]):
    result = NewYorkTimesWebsite.split_and_sanitise_byline(test_string)
    assert result == expected


@pytest.mark.parametrize(
    ("test_fields", "existing_identifiers", "expected"),
    (
        (
            {
                "date": DateField(date(2023, 6, 5)),
                "author": NameField("Serene Arc"),
                "organization": "New York Times",
            },
            (),
            "arc_2023_nyt",
        ),
        (
            {
                "date": DateField(date(2023, 6, 5)),
                "author": NameField("Serene Arc"),
                "organization": "New York Times",
            },
            ("arc_2023_nyt",),
            "arc_2023_nyt_1",
        ),
        (
            {
                "date": DateField(date(2023, 6, 5)),
                "author": NameField(
                    (
                        "Serene Arc",
                        "Test Testman",
                    )
                ),
                "organization": "New York Times",
            },
            ("arc_2023_nyt",),
            "arc_testman_2023_nyt",
        ),
        (
            {
                "date": DateField(date(2023, 6, 5)),
                "author": NameField(
                    (
                        "Serene Arc",
                        "Test Testman",
                        "John Doe",
                    )
                ),
                "organization": "New York Times",
            },
            (
                "arc_2023_nyt",
                "arc_testman_2023_nyt",
                "arc_testman_doe_2023_nyt",
            ),
            "arc_testman_doe_2023_nyt_1",
        ),
        (
            {
                "date": DateField(date(2023, 6, 5)),
                "author": NameField("Serene de la Arc"),
                "organization": "New York Times",
            },
            (),
            "arc_2023_nyt",
        ),
    ),
)
def test_generate_unique_identifier(
    test_fields: dict[str, str | BaseSpecialField],
    existing_identifiers: Sequence[str],
    expected: str,
):
    class TestNewYorkTimesWebsite(NewYorkTimesWebsite):
        def __init__(self, identifier: str):
            super().__init__(identifier, MagicMock())
            self.fields = test_fields

        def retrieve_information(self):
            pass

    test_source = TestNewYorkTimesWebsite("test")
    result = test_source.generate_unique_identifier(existing_identifiers)
    assert result == expected
