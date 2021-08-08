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


def test_db_update_by_id():
    db = DB(keys=["age", "name"])
    id1 = db.add({"name": "test", "age": 3})
    id2 = db.add({"name": "test2", "age": 4})

    db.update_by_id(id1, {"name": "changed"})
    db.update_by_id(id2, {"name": "updated", "age": 69})
    assert db._db[id1] == {"name": "changed", "age": 3}
    assert db._db[id2] == {"name": "updated", "age": 69}


@pytest.mark.parametrize(
    "test_input",
    (
        {"name2": "test"},
        {"name": "test", "test": "test"}
    )
)
def test_db_update_by_id_error(test_input):
    db = DB(keys=["age", "name"])
    id1 = db.add({"name": "test", "age": 3})

    with pytest.raises(KeyError):
        db.update_by_id(id1, test_input)


def test_db_update_by_query(db_w_data):
    assert list(db_w_data._db.values()) == DB_TEST_DATA

    db_w_data.update_by_query({"age": 1}, {"name": "changed"})
    assert list(db_w_data._db.values()) == [
        {"name": "changed", "age": 1},
        {"name": "fred", "age": 2},
        {"name": "mike", "age": 3},
        {"name": "steve", "age": 4},
        {"name": "changed", "age": 1},
    ]


@pytest.mark.parametrize(
    "q,v",
    (
        ({"age": 1}, {"test": "test"}),
        ({"test": 3}, {"age": 3}),
        ({"age": 1}, {"age": 3, "test": 3})
    )
)
def test_db_update_by_query_error(db_w_data, q, v):
    with pytest.raises(KeyError):
        db_w_data.update_by_query(q, v)
