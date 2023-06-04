import pytest

from omnicite.sources.articles.base_article import BaseArticle


@pytest.mark.online
@pytest.mark.parametrize(
    ("test_doi", "expected_dict_values"),
    (
        (
            "10.1590/0102-311x00133115",
            {
                "author": "Viroj Wiwanitki",
                "doi": "10.1590/0102-311x00133115",
                "journaltitle": "Cadernos de Saúde Pública",
                "month": 11,
                "number": "11",
                "publisher": "FapUNIFESP (SciELO)",
                "title": "Congenital Zika virus syndrome",
                "url": "https://doi.org/10.1590/0102-311x00133115",
                "volume": "32",
                "year": "2016",
            },
        ),
        (
            "https://doi.org/10.1177/21582440231178261",
            {
                "doi": "10.1177/21582440231178261",
                "url": "http://dx.doi.org/10.1177/21582440231178261",
                "year": "2023",
                "month": "4",
                "publisher": "SAGE Publications",
                "volume": "13",
                "number": "2",
                "pages": "215824402311782",
                "author": "Chigozie Nelson Nkalu and Chike Cletus Agu",
                "title": "Fiscal Policy and Economic Stabilization Dynamics in Sub-Saharan Africa: "
                "A New Evidence from Panel VEC Model and Hodrick-Prescott Filter Cyclical Decomposition",
                "journaltitle": "SAGE Open",
            },
        ),
    ),
)
def test_get_doi_information(test_doi: str, expected_dict_values: dict):
    result = BaseArticle.get_doi_information(test_doi)
    assert all([str(result[key]) == expected_dict_values[key] for key in expected_dict_values.keys()])
