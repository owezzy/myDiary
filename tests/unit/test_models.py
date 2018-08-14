import pytest

from app.app import EntryManager


@pytest.fixture(autouse=True)
def entymanager():
    entrymanager = EntryManager()
    return entrymanager


def test_last_id():
    last_id = 0
    assert (last_id == EntryManager.last_id)


def test_insert_entry(self, entry):
    self.__class__.last_id = id
    id += 1
    entry.id = self.__class__.last_id
    self.entries[self.__class__.last_id] = entry

    # user request for a single entry from entries list

    def get_entry(self, id):
        return self.entries[id]

    # user delete a single entry

    def delete_entry(self, id):
        return self.entries.pop(id)
