import os
from pathlib import Path

import pytest

from pysondb.utils import create_db
from pysondb.utils import verify_data


@pytest.fixture
def rm_file():
    yield
    os.remove("pysondb-test.json")


@pytest.fixture
def data_min():
    yield {"name": "test", "age": 4, "place": "canada"}


@pytest.mark.parametrize(
    "test_input",
    (
        {"name": "test", "place": "denmark", "age": 3},
        {"name": "ad", "age": 3, "place": "texas"},
    )
)
def test_verify_data(data_min, test_input):
    assert verify_data(data_min, test_input) is True


@pytest.mark.parametrize(
    "test_input",
    (
        {"name": "test"},
        {"name": "ad", "place": "texas", "age": 3, "location": "test"},
        {"name": "as", "place": "canada", "test": 3}
    )
)
def test_verify_data_failure(data_min, test_input):
    with pytest.raises(KeyError):
        _ = verify_data(data_min, test_input)


@pytest.mark.usefixtures("rm_file")
def test_create_db_file_does_not_exists():
    create_db("pysondb-test.json")
    assert Path("./pysondb-test.json").is_file()
