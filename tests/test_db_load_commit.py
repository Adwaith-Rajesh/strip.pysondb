import json
import os

import pytest

from pysondb.core import DB


DB_TEST_DATA = {
    "1": {"name": "ad", "age": 1},
    "13": {"name": "fred", "age": 2},
    "14": {"name": "mike", "age": 3},
}


def remove_file(): return os.remove("strip.pysondb.json")


@pytest.fixture
def rm_file():
    yield
    remove_file()


@pytest.fixture
def gen_json_file():
    with open("strip.pysondb.json", "w") as f:
        json.dump(DB_TEST_DATA, f)
    yield
    remove_file()


@pytest.mark.usefixtures("gen_json_file")
def test_db_load():
    db = DB(keys=["name", "age"])
    db.load("strip.pysondb.json")

    assert db._db == DB_TEST_DATA


@pytest.mark.usefixtures("rm_file")
def test_db_commit():
    db = DB(keys=["name", "age"])
    db._db = DB_TEST_DATA

    db.commit("strip.pysondb.json")

    with open("strip.pysondb.json", "r") as f:
        assert json.load(f) == DB_TEST_DATA
