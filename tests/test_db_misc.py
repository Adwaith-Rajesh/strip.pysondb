from pysondb.core import DB


def test_db_custom_id_add():

    count = 0

    def custom_id():
        nonlocal count
        count += 1
        return str(count)

    db = DB(keys=["name", "age"])
    db.set_id_generator(custom_id)

    for i in range(10):
        db.add({"name": f"name{i}", "age": i})

    assert db._id_generator == custom_id
    assert db._db == {'1': {'name': 'name0', 'age': 0},
                      '2': {'name': 'name1', 'age': 1},
                      '3': {'name': 'name2', 'age': 2},
                      '4': {'name': 'name3', 'age': 3},
                      '5': {'name': 'name4', 'age': 4},
                      '6': {'name': 'name5', 'age': 5},
                      '7': {'name': 'name6', 'age': 6},
                      '8': {'name': 'name7', 'age': 7},
                      '9': {'name': 'name8', 'age': 8},
                      '10': {'name': 'name9', 'age': 9}}


def test_db_custom_id_add_many():
    count = 0

    def custom_id():
        nonlocal count
        count += 1
        return str(count)

    db = DB(keys=["name", "age"])
    db.set_id_generator(custom_id)

    data = [{"name": f"name{i}", "age": i} for i in range(10)]
    db.add_many(data)

    assert db._id_generator == custom_id
    assert db._db == {'1': {'name': 'name0', 'age': 0},
                      '2': {'name': 'name1', 'age': 1},
                      '3': {'name': 'name2', 'age': 2},
                      '4': {'name': 'name3', 'age': 3},
                      '5': {'name': 'name4', 'age': 4},
                      '6': {'name': 'name5', 'age': 5},
                      '7': {'name': 'name6', 'age': 6},
                      '8': {'name': 'name7', 'age': 7},
                      '9': {'name': 'name8', 'age': 8},
                      '10': {'name': 'name9', 'age': 9}}


def test_db_len():
    db = DB(keys=["name"])
    assert len(db) == len(db._db) == 0

    db.add({"name": "ad"})
    assert len(db) == len(db._db) == 1

    db.add_many([{"name": f"name{i}"} for i in range(10)])
    assert len(db) == len(db._db) == 11
