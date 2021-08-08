import pytest

from pysondb.core import DB

DB_TEST_DATA = [
    {"name": "ad", "age": 1},
    {"name": "fred", "age": 2},
    {"name": "mike", "age": 3},
    {"name": "steve", "age": 4},
    {"name": "fit", "age": 1},
]


@pytest.fixture
def db_w_data():
    db = DB(keys=["name", "age"])
    db.add_many(DB_TEST_DATA)
    return db


def test_db_get_all(db_w_data):

    assert list(db_w_data.get_all().values()) == DB_TEST_DATA


def test_db_get_by_query(db_w_data):
    assert list(db_w_data.get_by_query({"age": 1}).values()) == [
        {"name": "ad", "age": 1},
        {"name": "fit", "age": 1},
    ]
    assert list(db_w_data.get_by_query({"name": "ad", "age": 1}).values()) == [
        {"name": "ad", "age": 1}
    ]


def test_db_get_by_id():
    db = DB(keys=["name", "age"])

    id1 = db.add({"name": "test", "age": 3})
    id2 = db.add({"name": "test2", "age": 2})

    assert db.get_by_id(id1) == {"name": "test", "age": 3}
    assert db.get_by_id(id2) == {"name": "test2", "age": 2}
    assert db.get_by_id("34") is None


def test_db_pop():
    db = DB(keys=["name", "age"])

    id1 = db.add({"name": "test", "age": 3})
    id2 = db.add({"name": "test2", "age": 2})

    assert len(db._db) == 2
    assert db.pop(id1) == {"name": "test", "age": 3}
    assert len(db._db) == 1
    assert db.pop(id2) == {"name": "test2", "age": 2}
    assert len(db._db) == 0
    assert db.pop("34") is None
