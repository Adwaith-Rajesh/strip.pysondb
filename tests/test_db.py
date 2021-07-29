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


def test_get_all():
    data = [{"name": f"name{1}", "age": i} for i in range(10)]
    db = DB("test.json", in_memory=True)
    db.add_many(data)

    assert len(db.get_all()) == 10
    assert list(db.get_all().values()) == data


def test_get_by_id():
    db = DB('test.json', in_memory=True)
    data = [{"name": f"name{1}", "age": i} for i in range(3)]

    id1 = db.add(data[0])
    id2 = db.add(data[1])
    id3 = db.add(data[2])

    assert db.get_by_id(id1) == data[0]
    assert db.get_by_id(id2) == data[1]
    assert db.get_by_id(id3) == data[2]
    assert db.get_by_id("3") is None


def test_get_by_query():
    db = DB("test.json", in_memory=True)
    data = [{"name": "test", "age": 1}, {
        "name": "test2", "age": 1}, {"name": "test", "age": 2}]

    db.add_many(data)

    assert len(db.get_by_query({"name": "test"})) == 2
    assert all((i in data for i in db.get_by_query({"name": "test"}).values()))

    assert len(db.get_by_query({"name": "test", "age": 1})) == 1
    assert list(db.get_by_query(
        {"name": "test", "age": 1}).values()) == [data[0]]

    assert db.get_by_query({"main": "test"}) == {}
