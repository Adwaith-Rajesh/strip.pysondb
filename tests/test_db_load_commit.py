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


@pytest.mark.usefixtures("gen_json_file")
def test_load_warning():
    db = DB(keys=["name", "age"])

    db.add({"name": "test", "age": 1})

    with pytest.warns(UserWarning):
        db.load("strip.pysondb.json")


@pytest.mark.usefixtures("gen_json_file")
def test_load_warning_force():

    db = DB(keys=["name", "age"])
    db.add({"name": "test", "age": 1})

    with pytest.warns(None):
        db.load("strip.pysondb.json", force=True)

    assert db._db == DB_TEST_DATA


@pytest.mark.usefixtures("gen_json_file")
def test_load_warning_after_commit():

    db = DB(keys=["name", "age"])
    db.add({"name": "test", "age": 1})

    db.commit("strip.pysondb.json")

    with pytest.warns(None):
        db.load("strip.pysondb.json")

    assert len(db._db) == 1


@pytest.mark.usefixtures("rm_file")
def test_load_json_decode_error():
    with open("strip.pysondb.json", "w") as f:
        f.write("{")

    db = DB(keys=[])

    try:
        db.load("strip.pysondb.json")

    except json.JSONDecodeError:
        pytest.fail("Json decode error raised while loading")

    assert db._db == {}


@ pytest.mark.usefixtures("gen_json_file")
def test_dynamic_loading():
    db = DB(keys=[], dynamic=True)
    db.load("strip.pysondb.json")

    assert db.keys == ["age", "name"]
    assert db._db == DB_TEST_DATA


@ pytest.mark.usefixtures("rm_file")
@ pytest.mark.parametrize(
    "data, keys",
    (
        ({}, []),
        ({"name": "test"}, []),
        ({}, ["name", "age"]),
        ({"name": "test"}, ["name", "age"])
    )


)
def test_dynamic_loading_handle_error(data, keys):
    with open("strip.pysondb.json", "w") as f:
        json.dump(data, f)
    db = DB(keys=keys, dynamic=True)
    try:
        db.load("strip.pysondb.json")
    except (IndexError, AttributeError) as e:
        pytest.fail(f"Error, raised in dynamic loading: {e}")

    assert db.keys == sorted(keys)


@ pytest.mark.usefixtures("rm_file")
def test_db_commit():
    db = DB(keys=["name", "age"])
    db._db = DB_TEST_DATA

    db.commit("strip.pysondb.json")

    with open("strip.pysondb.json", "r") as f:
        assert json.load(f) == DB_TEST_DATA
