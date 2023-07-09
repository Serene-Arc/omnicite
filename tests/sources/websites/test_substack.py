from datetime import date
from unittest.mock import MagicMock

import pytest

from omnicite.sources.websites.substack import Substack
from omnicite.special_fields.base_special_field import BaseSpecialField


@pytest.mark.asyncio
@pytest.mark.online
@pytest.mark.parametrize(
    ("test_url", "expected_dict"),
    (
        (
            "https://www.erininthemorning.com/p/top-5-states-to-be-transgender-in",
            {
                "author": "Erin Reed",
                "date": "2023-07-05",
                "organization": "Substack",
                "subtitle": "Transgender people are migrating across the country, and many are trying to decide"
                " which state they want to move to. This list shows the best states for being trans"
                " in 2023.",
                "title": "Top 5 States To Be Transgender In 2023",
                "url": "https://www.erininthemorning.com/p/top-5-states-to-be-transgender-in",
                "urldate": date.today().isoformat(),
            },
        ),
        (
            "https://www.erininthemorning.com/p/her-name-was-eden",
            {
                "author": "Erin Reed",
                "date": "2023-03-14",
                "organization": "Substack",
                "subtitle": "Eden was a transgender woman from Saudi Arabia. With the help of US-based private"
                " investigators, she was trafficked out of the country. 24 hours after her suicide,"
                " major media outlets stay silent.",
                "title": "Her Name Was Eden",
                "url": "https://www.erininthemorning.com/p/her-name-was-eden",
                "urldate": date.today().isoformat(),
            },
        ),
        (
            "https://fighttorepair.substack.com/p/from-farms-to-pharmaceuticals-its?utm_source=profile&utm_medium"
            "=reader2",
            {
                "author": "Paul Roberts",
                "date": "2023-07-07",
                "organization": "Substack",
                "subtitle": "From farms to drugstores to auto body shops, U.S. consumers are suffering under the"
                " thumb of corporate interests that have successfully engineered competition out of the"
                " marketplace.",
                "title": "From Farms to Pharmaceuticals: It’s the Monopoly, Stupid!",
                "url": "https://fighttorepair.substack.com/p/from-farms-to-pharmaceuticals-its?utm_source=profile"
                "&utm_medium=reader2",
                "urldate": date.today().isoformat(),
            },
        ),
        (
            "https://heathercoxrichardson.substack.com/p/july-6-2023",
            {
                "author": "Heather Cox Richardson",
                "date": "2023-07-07",
                "organization": "Substack",
                "subtitle": "",
                "title": "July 6, 2023",
                "url": "https://heathercoxrichardson.substack.com/p/july-6-2023",
                "urldate": date.today().isoformat(),
            },
        ),
    ),
)
async def test_make_source(
    test_url: str,
    expected_dict: dict[str, str | BaseSpecialField],
):
    test_source = await Substack.construct_source(test_url, MagicMock())
    assert all([str(test_source.fields[key]) == expected_dict[key] for key in expected_dict.keys()])
