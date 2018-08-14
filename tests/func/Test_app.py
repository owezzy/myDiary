import pytest
import json
from app.app import app


@pytest.fixture(scope='session')
def test_app():
    entrymanager = EntryManager()
    return entrymanager


def test_last_id():
    last_id = 0
    assert entymanager.last_id(last_id == 0)


def test_insert_enrty():
    pass


def test_get_entry():
    pass
