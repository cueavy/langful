"""
langful class
"""

import typing
import copy
import os

from . import default
from . import loader
from . import func

__all__ = ["langful"]


class langful:

    @property
    def locale(self) -> str:
        locales = [
            locale for locale in self.locale_defaults if locale in self.locales]
        if locales:
            return locales[0]
        else:
            raise KeyError(f"no locales are available")

    @property
    def locales(self) -> list[str]:
        return list(self.languages.keys())

    @property
    def language(self) -> dict[str, typing.Any]:
        return self.lazyloading(self.locale)

    def __getitem__(self, key: str) -> str:
        return self.get(key)

    def __setitem__(self, key: str, value: typing.Any) -> None:
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        self.remove(key)

    def __contains__(self, key: str) -> bool:
        return key in self.languages

    def __enter__(self) -> "langful":
        return self

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self.languages)

    def __exit__(self, *_: tuple[typing.Any, typing.Any, typing.Any]) -> None:
        self.save_all()

    def __bool__(self) -> bool:
        return self.locale_defaults[-2] in self.languages

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.languages)

    def __len__(self) -> int:
        return len(self.languages)

    def __init__(self, path: str | None = "lang", locale_default: str = "en_us", loader_langful: loader.loader_langful = default.loader_langful(), locale_get_func: typing.Callable[..., str] = func.getlocale, lazyload: bool = False) -> None:
        self.locale_defaults: list[str] = [
            "", locale_get_func(), locale_default]
        self.languages: dict[str, dict[str, typing.Any] | loader.Lazyload] = {}
        self.locale_get_func = locale_get_func
        self.loader: loader.loader_langful = loader_langful
        self.types: dict[str, str] = {}
        self.path: str = "" if path is None else path
        self.lazyload: bool = lazyload
        if path and os.path.isdir(path):
            self.load_all(path)

    def load(self, file: str) -> None | Exception:
        name = os.path.splitext(os.path.split(file)[-1])[0]
        try:
            data = self.loader.lazyload(
                file) if self.lazyload else self.loader.load(file)
        except Exception as e:
            return e
        self.types[name] = file
        self.languages[name] = data

    def load_all(self, path: str) -> None | tuple[tuple[str, Exception], ...]:
        ret: list[tuple[str, Exception]] = []
        if not os.path.isdir(path):
            raise NotADirectoryError(
                "the path is not exist or not a directory")
        for file in os.listdir(path):
            file = os.path.join(path, file)
            if os.path.isfile(file):
                e = self.load(file)
                if e:
                    ret.append((file, e))
        return tuple(ret) if ret else None

    def lazyloading(self, locale: str | None = None) -> dict[str, typing.Any]:
        return self.get_language(locale)

    def lazyloading_all(self) -> None:
        for locale in self.locales:
            self.lazyloading(locale)

    def save(self, locale: str | None = None, file: str | None = None, suffix: str | None = None) -> None | Exception:
        locale = self.get_locale(locale)
        if file is None:
            file = self.types[locale]
        try:
            self.loader.save(file, self.get_language(locale), suffix)
        except Exception as e:
            return e

    def save_all(self, path: str | None = None) -> None | tuple[tuple[str, Exception], ...]:
        ret: list[tuple[str, Exception]] = []
        if path:
            if not os.path.isdir(path):
                raise NotADirectoryError(
                    "the path is exist but not a directory")
            if not os.path.exists(path):
                os.makedirs(path)
        for locale, file in self.types.items():
            if path:
                file = os.path.join(path, os.path.split(file)[-1])
            e = self.save(locale, file)
            if e:
                ret.append((file, e))
        return tuple(ret) if ret else None

    def reset_locale_defaults(self, locale_default: str | None = None) -> None:
        self.locale_defaults = ["", self.locale_get_func(
        ), self.locale_defaults[-1] if locale_default is None else locale_default]

    def reset_languages(self) -> None:
        self.languages.clear()
        self.types.clear()

    def reset(self) -> None:
        self.reset_locale_defaults()
        self.reset_languages()

    def values(self) -> tuple[dict[str, typing.Any] | loader.Lazyload, ...]:
        return tuple(self.languages.values())

    def items(self) -> tuple[tuple[str, dict[str, typing.Any] | loader.Lazyload], ...]:
        return tuple(zip(self.keys(), self.values()))

    def keys(self) -> tuple[str, ...]:
        return tuple(self.languages.keys())

    def merge(self, *locales: str) -> dict[str, typing.Any]:
        if len(locales) < 1:
            raise IndexError("out of the locales range")
        language = copy.deepcopy(self.get_language(locales[-1]))
        for locale in locales[: -1][:: -1]:
            for key, value in self.get_language(locale).items():
                if key not in language:
                    language[key] = value
        return language

    def merge_all(self, locale_default: str | None = None) -> None:
        if locale_default is None:
            locale_default = self.locale_defaults[-1]
        if locale_default in self.locales:
            locales = copy.deepcopy(self.locales)
            locales.remove(locale_default)
            for locale in locales:
                self.set_language(self.merge(locale_default, locale), locale)
        else:
            raise KeyError("the default locale is not in the locales")

    def differ(self, locale_base: str, *locales: str) -> dict[str, typing.Any]:
        keys = set(self.merge(*locales).keys())
        return {key: value for key, value in self.get_language(locale_base).items() if key not in keys}

    def replace(self, key: str, data: dict[str, typing.Any], default: str = "", locale: str | None = None) -> str:
        ret: list[str] = []
        tmp: list[str] = []
        escape = False
        replace = False
        for char in str(self.get(key, locale)):
            if escape:
                if char in ("{", "}"):
                    ret.append(char)
                else:
                    ret.append(f"\\{char}")
                escape = False
            elif char == "\\":
                escape = True
            elif replace:
                if char == "}":
                    ret.append(str(data.get("".join(tmp).strip(), default)))
                    replace = False
                    tmp = []
                else:
                    tmp.append(char)
            else:
                if char == "{":
                    replace = True
                else:
                    if tmp:
                        ret.append("".join(tmp))
                        tmp = []
                    ret.append(char)
        if tmp:
            ret.append("".join(tmp))
        return "".join(ret)

    def get(self, key: str, locale: str | None = None) -> typing.Any:
        return self.get_language(locale)[key]

    def get_language(self, locale: str | None = None) -> dict[str, typing.Any]:
        locale = self.get_locale(locale)
        language = self.languages[locale]
        if isinstance(language, loader.Lazyload):
            language = language.load()
            self.languages[locale] = language
        return language

    def get_type(self, locale: str | None = None) -> str:
        return self.types[self.get_locale(locale)]

    def get_locale(self, locale: str | None = None) -> str:
        return self.locale if locale is None else locale

    def set(self, key: str, value: typing.Any, locale: str | None = None) -> None:
        self.get_language(locale)[key] = value

    def set_language(self, data: dict[str, typing.Any] = {}, locale: str | None = None, type: str | None = None) -> None:
        self.languages[self.get_locale(locale)] = data
        if type is not None:
            self.set_type(type)

    def set_type(self, type: str = ".json", locale: str | None = None) -> None:
        self.types[self.get_locale(locale)] = type

    def set_locale(self, locale: str = "") -> None:
        self.locale_defaults[0] = locale

    def remove(self, key: str, locale: str | None = None) -> None:
        del self.get_language(locale)[key]

    def remove_language(self, locale: str | None = None) -> None:
        del self.languages[self.get_locale(locale)]
        self.remove_type(locale)

    def remove_type(self, locale: str | None = None) -> None:
        del self.types[self.get_locale(locale)]

    def remove_locale(self) -> None:
        self.locale_defaults[0] = ""

    def pop(self, key: str, locale: str | None = None) -> typing.Any:
        ret = self.get(key, locale)
        self.remove(key, locale)
        return ret

    def pop_language(self, locale: str | None = None) -> dict[str, typing.Any]:
        ret = self.get_language(locale)
        self.remove_language(locale)
        return ret

    def pop_type(self, locale: str | None = None) -> str:
        ret = self.get_type(locale)
        self.remove_type(locale)
        return ret

    def pop_locale(self) -> str:
        ret = self.get_locale()
        self.remove_locale()
        return ret
