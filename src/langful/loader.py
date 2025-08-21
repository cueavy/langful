"""
loader
"""

import typing
import os

from . import parser

__all__ = ["Lazyload", "loader_langful", "loader_assetful"]


class Lazyload:

    def __init__(self, func: typing.Callable[..., typing.Any], *args: typing.Any, **kwargs: dict[str, typing.Any]) -> None:
        self.func: typing.Callable[..., typing.Any] = func
        self.args: tuple[typing.Any, ...] = args
        self.kwargs: dict[str, typing.Any] = kwargs

    def load(self) -> typing.Any:
        return self.func(*self.args, **self.kwargs)


class loader_langful:

    def __contains__(self, key: str) -> bool:
        return key in self.suffixes

    def __getitem__(self, key: str) -> parser.parser_langful:
        return self.suffixes[key]

    @property
    def suffixes(self) -> dict[str, parser.parser_langful]:
        suffixes: dict[str, parser.parser_langful] = {}
        for p in self.parsers:
            suffixes.update({suffix: p for suffix in (
                p.suffix if isinstance(p.suffix, tuple) else (p.suffix, ))})
        return suffixes

    def __init__(self) -> None:
        self.parsers: list[parser.parser_langful] = []

    def load(self, file: str, suffix: str | None = None) -> dict[str, typing.Any]:
        if suffix is None:
            suffix = os.path.splitext(file)[-1]
        if suffix not in self:
            raise KeyError(f"no parser can load file with '{suffix}' suffix")
        if not os.path.exists(file):
            raise FileNotFoundError("the file is not exist")
        elif not os.path.isfile(file):
            raise IsADirectoryError("the path is exist but not a file")
        return self.suffixes[suffix].load(file)

    def lazyload(self, file: str, suffix: str | None = None) -> Lazyload:
        return Lazyload(self.load, file, suffix)

    def save(self, file: str, data: dict[str, typing.Any], suffix: str | None = None) -> None:
        if os.path.exists(file) and not os.path.isfile(file):
            raise IsADirectoryError("the path is not a file")
        if suffix is None:
            suffix = os.path.splitext(file)[-1]
        if suffix not in self:
            raise KeyError(f"no parser can load file with '{suffix}' suffix")
        self.suffixes[suffix].save(data, file)


class loader_assetful:
    pass
