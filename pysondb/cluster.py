import json
import warnings
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from .core import DB

ClusterDataType = Dict[str,
                       Dict[str, Union[List[str], Dict[str, Dict[str, Any]]]]]


class Cluster:
    """Use multiple DB from a single entry point"""

    def __init__(self, dbs: Dict[str, DB], dynamic: bool = False) -> None:

        self._dbs: Dict[str, DB] = dbs
        self._d_loading = dynamic
        self._verify_dbs()

    def __repr__(self) -> str:
        return f"A Cluster of {{ {', '.join(self._dbs)} }}"

    def __getattr__(self, k: object) -> Union[DB, None]:
        if isinstance(k, str):
            return self._dbs.get(k)

        return None

    def __getitem__(self, k: object) -> Union[DB, None]:
        if isinstance(k, str):
            return self._dbs.get(k)

        return None

    @property
    def databases(self) -> List[str]:
        """Returns the names of all the DB's in the cluster"""
        return sorted(list(self._dbs))

    def _verify_dbs(self) -> None:

        if not self._d_loading:
            if self._dbs:
                if not all(isinstance(j, str) for j in self._dbs):
                    raise KeyError("All the keys must be a string.")
                if not all(isinstance(i, DB) for i in self._dbs.values()):
                    raise ValueError("All the values must be of type 'DB'")

            else:
                raise ValueError("Cluster intialized with empty DB data")

    def commit(self, filename: str, indent: Optional[int] = None) -> None:
        """commmit all the data from all the db to a single file"""
        data: ClusterDataType = {}
        for db in self._dbs:
            data[db] = {}
            data[db]["keys"] = self._dbs[db].keys
            data[db]["data"] = self._dbs[db]._db

        with open(filename, "w") as f:
            json.dump(data, f, indent=indent)

    def load(self, filename: str) -> None:
        """load the cluster"""
        if Path(filename).is_file():
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    warnings.warn(UserWarning(
                        f"Error while decoding {filename!r}."), stacklevel=2)
                    self._dbs = {}
                    return None

            if self._d_loading:
                # Create the DBs dict
                self._dbs = {i: DB(keys=[]) for i in data}

                # add the to the DB in the cluster
                for d in self._dbs:
                    self._dbs[d]._keys = sorted(data[d]["keys"])

            # verify and add the data to the DB
            req_data: Dict[str, Dict[str, Dict[str, Any]]] = {
                i: data[i]["data"] for i in self._dbs}

            # verify
            for rk, rv in req_data.items():

                try:
                    for v in rv.values():
                        self._dbs[rk]._verify_data(v)
                except KeyError:
                    raise KeyError(f"The key provided for the DB {rk!r} -> ({self._dbs[rk].keys})"
                                   f" does not match the keys in the cluster data ({list(v.keys())})") from None

            # add the data to DB
            for rk, rv in req_data.items():
                self._dbs[rk]._db = rv.copy()
