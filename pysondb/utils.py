import uuid
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List


def verify_data(v_data: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """
    v_data: The data we trust.
    data: The data to verify
    """
    if sorted(v_data.keys()) == sorted(data.keys()):
        return True

    else:
        raise KeyError(
            f"The keys provided in the data does not comply with the keys in the DB: {list(v_data.keys())}")


def create_db(filename: str) -> None:
    """Create a JSON DB file it doesn't exist"""
    if not Path(filename).is_file() is True and filename.endswith(".json"):
        with open(filename, "w") as f:
            f.write("{}")


def generate_id(keys: List[str]) -> str:

    def gen_id() -> str:
        _id = str(uuid.uuid4().int)[:16]
        if _id not in keys:
            return _id

        else:
            return gen_id()

    return gen_id()
