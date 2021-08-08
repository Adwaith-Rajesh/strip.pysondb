import pytest

from pysondb.core import DB


@pytest.fixture
def db():
    # a normal age, name db
    return DB(keys=["name", "age"])


def test_db_add(db):
    assert len(db._db) == 0
    db.add({"name": "ad", "age": 2})
    assert len(db._db) == 1
    db.add({"name": "fred", "age": 2})
    assert len(db._db) == 2


@pytest.mark.parametrize(
    "test_input",
    (
        {"name": "test"},
        {"name": "test", "age": 3, "test": "test"},
        {"a": 1}
    )
)
def test_add_error(db, test_input):
    with pytest.raises(KeyError):
        db.add(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        {"name": "test"},
        {"name": "test", "age": 3, "test": "test"},
        {"a": 1}
    )
)
def test_db_add_no_verify(test_input):
    db = DB(keys=["name", "age"], verify_data=False)

    try:
        db.add(test_input)
    except KeyError:
        pytest.raises("Key error was raised in db.add, with no verify")


def test_db_add_many(db):
    assert len(db._db) == 0

    db.add_many(
        [
            {"name": "test", "age": 1},
            {"name": "test1", "age": 2},
            {"name": "test2", "age": 3},
        ]
    )

    assert len(db._db) == 3


@pytest.mark.parametrize(
    "test_input",
    (
        [{"name": "test"}],
        [{"name": "test", "age": 2}, {"name": "test"}]
    )
)
def test_db_add_many_error(db, test_input):
    with pytest.raises(KeyError):
        db.add_many(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        [{"name": "test"}],
        [{"name": "test", "age": 2}, {"name": "test"}]
    )
)
def test_db_add_many_no_verify(test_input):
    db = DB(keys=["name", "age"], verify_data=False)

    try:
        db.add_many(test_input)

    except KeyError:
        pytest.fail("KeyError was raised in db.add_many, no verify")
