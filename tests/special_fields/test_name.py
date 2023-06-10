import pytest

from omnicite.special_fields.name import Name


@pytest.mark.parametrize(
    ("test_raw_name", "expected"),
    (
        ("al-Qadi al-Nu'man", "al-Qadi al-Nu'man"),
        ("al-qadi al-nu'man", "al-Qadi al-Nu'man"),
        ("c. s. Lewis", "C. S. Lewis"),
        ("C.S. Lewis", "C. S. Lewis"),
        ("c.s. Lewis", "C. S. Lewis"),
        ("Chigozie Nelson Nkalu", "Chigozie Nelson Nkalu"),
        ("CS Lewis", "C. S. Lewis"),
        ("CS lewis", "C. S. Lewis"),
        ("Guillermo de la Cruz", "Guillermo de la Cruz"),
        ("Guillermo del Toro", "Guillermo del Toro"),
        ("IV Testman", "I. V. Testman"),
        ("Johann Wolfgang von Goethe", "Johann Wolfgang von Goethe"),
        ("johann wolfgang von goethe", "Johann Wolfgang von Goethe"),
        ("John Doe III", "John Doe III"),
        ("john doe iii", "John Doe III"),
        ("John Doe IV", "John Doe IV"),
        ("john doe iv", "John Doe IV"),
        ("John Doe Jr.", "John Doe Jr."),
        ("John Doe", "John Doe"),
        ("john doe", "John Doe"),
        ("John Doe, Jr.", "John Doe Jr."),
        ("John Ronald Reuel Tolkien", "John Ronald Reuel Tolkien"),
        ("Joseph Gordon-Levitt", "Joseph Gordon-Levitt"),
        ("joseph gordon-levitt", "Joseph Gordon-Levitt"),
        ("Muhammad ibn Idris al-Shafii", "Muhammad ibn Idris al-Shafii"),
        ("muhammad ibn idris al-shafii", "Muhammad ibn Idris al-Shafii"),
        ("Ravindra V Adivarekar", "Ravindra V. Adivarekar"),
        ("Ravindra V. Adivarekar", "Ravindra V. Adivarekar"),
        ("Simon Simon", "Simon Simon"),
        ("{Federal Government of Australia}", "Federal Government of Australia"),
    ),
)
def test_format_to_string(test_raw_name: str, expected: str):
    test_name = Name(test_raw_name)
    assert str(test_name) == expected


@pytest.mark.parametrize(
    ("test_raw_name", "expected"),
    (
        ("al-Qadi al-Nu'man", "al-Nu'man"),
        ("Chigozie Nelson Nkalu", "Nkalu"),
        ("CS Lewis", "Lewis"),
        ("Guillermo del Toro", "del Toro"),
        ("John Doe", "Doe"),
        ("John Ronald Reuel Tolkien", "Tolkien"),
        ("Muhammad ibn Idris al-Shafii", "al-Shafii"),
        ("Ravindra V. Adivarekar", "Adivarekar"),
        ("Simon Simon", "Simon"),
        ("{Federal Government of Australia}", "Federal Government of Australia"),
    ),
)
def test_get_family_name(test_raw_name: str, expected: str):
    test_name = Name(test_raw_name)
    assert test_name.family_name == expected
