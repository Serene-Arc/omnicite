import pytest

from omnicite.exceptions import OmniCiteSourceException
from omnicite.sources.books.raw_isbn import RawISBN
from omnicite.special_fields.base_special_field import BaseSpecialField


@pytest.mark.online
@pytest.mark.parametrize(
    ("test_identifier", "expected_dict"),
    (
        (
            "9780261102378",
            {
                "author": "John Ronald Reuel Tolkien",
                "title": "The Return Of The King",
                "isbn": "9780261102378",
                "year": "2007",
                "publisher": "HarperCollins UK",
            },
        ),
    ),
)
def test_make_source(test_identifier: str, expected_dict: dict[str | BaseSpecialField]):
    test_source = RawISBN(test_identifier)
    assert all([str(test_source.fields[key]) == expected_dict[key] for key in expected_dict.keys()])


@pytest.mark.parametrize(
    "test_identifier",
    (
        "",
        "example",
        "123456",
    ),
)
def test_make_source_bad_isbn(test_identifier: str):
    with pytest.raises(OmniCiteSourceException) as exc:
        RawISBN(test_identifier)
    assert "not a valid ISBN" in str(exc.value)
