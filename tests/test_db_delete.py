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


def test_db_delete_by_id():
    db = DB(keys=["name", "age"])
    id1 = db.add({"name": "test", "age": 3})
    id2 = db.add({"name": "test2", "age": 4})

    assert len(db._db) == 2
    db.delete_by_id(id1)
    assert len(db._db) == 1
    db.delete_by_id(id2)
    assert len(db._db) == 0


def test_db_delete_by_query(db_w_data):
    assert len(db_w_data._db) == 5
    db_w_data.delete_by_query({"age": 1})
    assert len(db_w_data._db) == 3
    assert list(db_w_data._db.values()) == [{"name": "fred", "age": 2},
                                            {"name": "mike", "age": 3},
                                            {"name": "steve", "age": 4}, ]


def test_db_delete_all(db_w_data):
    assert len(db_w_data._db) == 5
    db_w_data.delete_all()
    assert len(db_w_data._db) == 0
