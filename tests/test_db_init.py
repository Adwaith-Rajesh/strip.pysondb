from pysondb.core import DB


def test_init_only_keys():
    db = DB(keys=["name", "age"])

    assert db._keys == ["age", "name"]
    assert db._verify is True
    assert db._db == {}
    assert db._id_generator == db._generate_id


def test_init_keys_and_verify():
    db = DB(keys=["name", "age"], verify_data=False)

    assert db._keys == ["age", "name"]
    assert db._verify is False
    assert db._db == {}
    assert db._id_generator == db._generate_id
