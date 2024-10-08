import pytest


@pytest.fixture(autouse=True)
def aaa_db(db):
    """Using this fixture makes the db available to all tests."""
