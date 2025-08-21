<div align = "center" >
    <h1>langful</h1>
    <a href = "https://pypi.org/project/langful" >
        <img alt = "PyPI version" src = "https://img.shields.io/pypi/v/langful?color=blue" >
    </a>
    <a href = "https://www.python.org" >
        <img alt = "Python version" src = "https://img.shields.io/badge/python-3.10+-blue" >
    </a>
    <a href = "https://opensource.org/license/mit" >
        <img alt = "license" src = "https://img.shields.io/badge/license-MIT-blue" >
    </a>
    <a href = "https://github.com/cueavy/langful" >
        <img alt = "Github issues" src = "https://img.shields.io/github/issues/cueavy/langful?color=blue" >
    </a>
    <hr>
        <p>[ English | <a href = "./README-zh_cn.md" >简体中文</a> ]</p>
    <hr>
</div>

# About

This is a simple module which is used for internationalization(i18n).

You just need place localization files in a directory, like this:

- lang
- - en_us.json
- - zh_cn.json

```python
import langful

lang = langful( "lang" )

print( lang )

```

The default language code is obtained using the `locale` module and follows the [RFC 1766](https://datatracker.ietf.org/doc/html/rfc1766.html) standard.

`langful` supports three default localization file types, and you can easily add custom loaders.

# Install

`pip install langful`

# Links

[
[github](https://github.com/cueavy/langful)
|
[pypi](https://pypi.org/project/langful)
]
