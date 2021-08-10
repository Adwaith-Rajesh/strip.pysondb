import json
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from .core import DB


class Cluster:
    """Use multiple DB from a single entry point"""

    def __init__(self, dbs: Dict[str, DB]) -> None:

        self._dbs: Dict[str, DB] = dbs
        self._verify_dbs()

    def __repr__(self) -> str:
        return f"A Cluster of {{ {', '.join(self._dbs)} }}"

    def __getattr__(self, k: str) -> Union[DB, None]:
        return self._dbs.get(k)

    def _verify_dbs(self) -> None:

        if self._dbs:
            if not all(isinstance(j, str) for j in self._dbs):
                raise KeyError("All the keys must be a string.")
            if not all(isinstance(i, DB) for i in self._dbs.values()):
                raise ValueError("All the values must be of type 'DB'")

        else:
            raise ValueError("Cluster intialized with empty DB data")

    def commit(self, filename: str, indent: Optional[int] = None) -> None:
        """commmit all the data from all the db to a single file"""
        data = {}
        for db in self._dbs:
            data[db] = self._dbs[db]._db

        with open(filename, "w") as f:
            json.dump(data, f, indent=indent)

    def load(self, filename: str) -> None:
        """load the cluster"""
        if Path(filename).is_file():
            try:
                with open(filename, "r") as f:
                    data = json.load(f)

                    req_data: Dict[str, Dict[str, Dict[str, Any]]] = {
                        i: data[i] for i in self._dbs if i in data}

                    for rd, rv in req_data.items():
                        try:
                            for v in rv.values():
                                self._dbs[rd]._verify_data(v)
                        except KeyError:
                            raise KeyError(
                                f"The key provided for the DB {rd!r} -> ({self._dbs[rd]._keys})"
                                f" does not match the keys in the cluster data ({list(v.keys())})") from None

                    for rd, rv in req_data.items():
                        self._dbs[rd]._db = rv.copy()

            except json.decoder.JSONDecodeError:
                pass
