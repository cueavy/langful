<div align="center">
    <h1>langful</h1>
    <a href = "https://pypi.org/project/langful" >
        <img alt = "PyPI version" src = "https://img.shields.io/pypi/v/langful?color=blue" >
    </a>
    <a href = "https://www.python.org" >
        <img alt = "Python version" src = "https://img.shields.io/badge/python-3.6+-blue" >
    </a>
    <a href = "https://opensource.org/license/mit" >
        <img alt = "license" src = "https://img.shields.io/badge/license-MIT-blue" >
    </a>
    <a href = "https://github.com/cueavyqwp/langful" >
        <img alt = "Github stars" src = "https://img.shields.io/github/stars/cueavyqwp/langful?color=blue" >
    </a>
    <a href = "https://github.com/cueavyqwp/langful" >
        <img alt = "Github issues" src = "https://img.shields.io/github/issues/cueavyqwp/langful?color=blue" >
    </a>
</div>

# install

`pip3 install langful` or `pip install langful`

# vscode-langful

[GitHub](https://github.com/cueavy/vscode-langful)

[VSCode](https://marketplace.visualstudio.com/items?itemName=cueavyqwp.langful)

# get start

## lang file

> ps: `langful` load json file first

### .json

```json
{
    "key": "value" ,
    "..." : "..."
}
```

### .lang

```
key = value # hi, this is a example
# hi, I am a example, too
... = ...
```

## init

there have `two` ways to init

> by files

```python
import langful
lang = langful.lang()
```

> by dictionary

```python
import langful
lang = langful.lang( False )
lang.init_dict( {
    "en_us" : {
        "hi" : "Hi" ,
        "welcome" : "Welcome"
    } ,
    "zh_cn" : {
        "hi" : "你好" ,
        "welcome" : "欢迎"
    }
} )
```

## replace

have bug

<!-- ```python
import langful
lang = langful.lang( False )
lang.init_dict( {
    "en_us" : {
        "hi" : "Hi" ,
        "welcome" : "Welcome"
    } ,
    "zh_cn" : {
        "hi" : "你好" ,
        "welcome" : "欢迎"
    }
} )
``` -->

## replace str

```python
import langful
lang = langful.lang( False )
lang.init_dict( {
    "en_us" : {
        "hi" : "Hi" ,
        "welcome" : "Welcome"
    } ,
    "zh_cn" : {
        "hi" : "你好" ,
        "welcome" : "欢迎"
    }
} )
print(lang.replace_str( "%hi%, %welcome%!" ))
```

# About

github: https://github.com/cueavyqwp/langful

pypi: https://pypi.org/project/langful

issues: https://github.com/cueavyqwp/langful/issues