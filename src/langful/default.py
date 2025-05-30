"""
default loader
"""

import typing
import json
import csv

from . import loader
from . import parser

__all__ = ["JSON", "LANG", "CSV", "loader_langful"]


class JSON(parser.parser_langful):

    def __init__(self) -> None:
        super().__init__()
        self.suffix = ".json"
        self.kwargs: dict[str, typing.Any] = {
            "ensure_ascii": False, "indent": 4, "separators": (",", ": ")}

    def load(self, path: str) -> dict[str, typing.Any]:
        with open(path, "rb") as fp:
            return json.load(fp)

    def save(self, data: dict[str, typing.Any], path: str) -> None:
        with open(path, "w", encoding="utf-8") as fp:
            json.dump(data, fp, **self.kwargs)


class LANG(parser.parser_langful):

    def __init__(self) -> None:
        super().__init__()
        self.suffix = ".lang"

    def load(self, path: str) -> dict[str, typing.Any]:
        ret: dict[str, typing.Any] = {}
        with open(path, "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                index = line.rfind("#")
                if index != -1:
                    line = line[: index]
                key, sep, value = line.partition("=")
                if sep == "":
                    continue
                ret[key.strip()] = format(value.strip())
        return ret

    def save(self, data: dict[str, typing.Any], path: str) -> None:
        with open(path, "w", encoding="utf-8") as fp:
            for key, value in data.items():
                fp.write(f"{key} = {value}\n")


class CSV(parser.parser_langful):

    def __init__(self) -> None:
        super().__init__()
        self.suffix = ".csv"

    def load(self, path: str) -> dict[str, typing.Any]:
        ret: dict[str, typing.Any] = {}
        with open(path, "r", encoding="utf-8") as fp:
            reader = csv.reader(fp)
            for row in reader:
                if len(row) >= 2:
                    ret[row[0]] = row[1]
        return ret

    def save(self, data: dict[str, typing.Any], path: str) -> None:
        with open(path, "w", encoding="utf-8", newline="") as fp:
            writer = csv.writer(fp)
            for key, value in data.items():
                writer.writerow((key, value))


class loader_langful(loader.loader_langful):

    def __init__(self) -> None:
        super().__init__()
        self.parsers = [JSON(), LANG(), CSV()]
