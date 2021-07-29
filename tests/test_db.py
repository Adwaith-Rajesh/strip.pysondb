import pytest

from pysondb.core import DB


def test_add():
    db = DB("test.json", in_memory=True)
    db.add({"name": "test", "age": 10})

    assert len(db._db) == 1
    assert list(db._db.values())[0] == {"name": "test", "age": 10}


def test_add_failure():
    db = DB("test.json", in_memory=True)
    db.add({
        "name": "test", "age": 4
    })

    with pytest.raises(KeyError):
        db.add({"name": "test"})

    with pytest.raises(KeyError):
        db.add({"name": "test", "age": 4, "test": 3})


def test_add_many():
    data = [{"name": f"name{1}", "age": i} for i in range(10)]

    db = DB("test.json", in_memory=True)
    db.add_many(data)

    assert len(db._db) == 10
    assert list(db._db.values()) == data


def test_add_many_failure():
    data = [{"name": f"name{1}", "age": i}
            for i in range(10)] + [{"name": "test"}]
    db = DB("test.json", in_memory=True)

    with pytest.raises(KeyError):
        db.add_many(data)
