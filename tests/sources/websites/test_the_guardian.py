from datetime import date
from typing import Sequence
from unittest.mock import MagicMock

import pytest
from confuse import Configuration

from omnicite.sources.websites.the_guardian import TheGuardian
from omnicite.special_fields.base_special_field import BaseSpecialField
from omnicite.special_fields.date_field import DateField
from omnicite.special_fields.name_field import NameField


@pytest.mark.asyncio
@pytest.mark.online
@pytest.mark.parametrize(
    ("test_url", "expected_dict"),
    (
        (
            "https://www.theguardian.com/us-news/2023/jun/09/donald-trump-indictment-unsealed-mar-a-lago",
            {
                "author": "Hugo Lowell and Léonie Chao-Fong",
                "date": "2023-06-10",
                "subtitle": "Trump took steps to retain classified documents subpoenaed by the justice department,"
                " according to indictment",
                "title": "Indictment charging Trump with mishandling classified documents unsealed",
                "url": "https://www.theguardian.com/us-news/2023/jun/09/donald-trump-indictment-unsealed-mar-a-lago",
                "urldate": date.today().isoformat(),
            },
        ),
        (
            "https://www.theguardian.com/environment/2023/jun/10/australia-firefighters-fire-crews-prepare-for-return-of-el-nino-bushfire-season-smoke-hazard-reduction-burns",
            {
                "author": "Graham Readfearn",
                "title": "Smoke in the air as Australia’s fire crews prepare for the return of El Niño",
                "subtitle": "Climate change has lengthened fire seasons and limited chances for hazard reduction burns, leaving authorities racing the clock before risky weather hits",
                "date": "2023-06-10",
                "url": "https://www.theguardian.com/environment/2023/jun/10/australia-firefighters-fire-crews-prepare-for-return-of-el-nino-bushfire-season-smoke-hazard-reduction-burns",
            },
        ),
    ),
)
async def test_make_source(
    test_url: str,
    expected_dict: dict[str, str | BaseSpecialField],
    test_configuration: Configuration,
):
    test_source = await TheGuardian.construct_source(test_url, test_configuration)
    assert all([str(test_source.fields[key]) == expected_dict[key] for key in expected_dict.keys()])


@pytest.mark.parametrize(
    ("test_fields", "existing_identifiers", "expected"),
    (
        (
            {
                "author": NameField(["Hugo Lowell", "Léonie Chao-Fong"]),
                "date": DateField(date(2023, 6, 10)),
            },
            (),
            "lowell_2023_guardian",
        ),
        (
            {
                "author": NameField(["Hugo Lowell", "Léonie Chao-Fong"]),
                "date": DateField(date(2023, 6, 10)),
            },
            ("lowell_2023_guardian",),
            "lowell_chaofong_2023_guardian",
        ),
    ),
)
def test_generate_unique_identifier(
    test_fields: dict[str, str | BaseSpecialField],
    existing_identifiers: Sequence[str],
    expected: str,
):
    class TestTheGuardian(TheGuardian):
        def __init__(self, identifier: str):
            super().__init__(identifier)
            self.fields = test_fields

        async def retrieve_information(self, _):
            pass

    test_source = TestTheGuardian("test")
    result = test_source.generate_unique_identifier(existing_identifiers)
    assert result == expected
