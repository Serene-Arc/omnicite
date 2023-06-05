import confuse
import pytest


@pytest.fixture(scope="session")
def test_configuration() -> confuse.Configuration:
    config = confuse.Configuration("OmniCite")
    config.set_file("tests/test_config.yaml")

    return config
