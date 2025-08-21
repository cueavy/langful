"""
parser
"""

import typing
import abc

__all__ = ["parser_langful", "parser_assetful"]


class parser_langful(abc.ABC):

    def __init__(self) -> None:
        self.suffix: tuple[str] | str

    @abc.abstractmethod
    def load(self, path: str) -> dict[str, typing.Any]:
        pass

    @abc.abstractmethod
    def save(self, data: dict[str, typing.Any], path: str) -> None:
        pass


class parser_assetful(abc.ABC):

    def __init__(self) -> None:
        pass
