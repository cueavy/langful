<div align = "center" >
    <h1>langful</h1>
    <a href = "https://pypi.org/project/langful" >
        <img alt = "PyPI version" src = "https://img.shields.io/pypi/v/langful?color=blue" >
    </a>
    <a href = "https://www.python.org" >
        <img alt = "Python version" src = "https://img.shields.io/badge/python-3.9+-blue" >
    </a>
    <a href = "https://opensource.org/license/mit" >
        <img alt = "license" src = "https://img.shields.io/badge/license-MIT-blue" >
    </a>
    <a href = "https://github.com/cueavy/langful" >
        <img alt = "Github stars" src = "https://img.shields.io/github/stars/cueavy/langful?color=blue" >
    </a>
    <a href = "https://github.com/cueavy/langful" >
        <img alt = "Github issues" src = "https://img.shields.io/github/issues/cueavy/langful?color=blue" >
    </a>

---

[
en_us
|
[zh_cn](./README-zh_cn.md)
]

---

</div>

# install

`pip3 install langful` or `pip install langful`

# get start

## lang file

> ps: `langful` load json file first
>
> or you can set to `langful.lang( json_first = False )`

.json

```json
{
    "key": "value" ,
    "..." : "..."
}
```

.lang

> if you need highlight, you can install `vscode-langful` :
[GitHub](https://github.com/cueavy/vscode-langful)
[VSCode](https://marketplace.visualstudio.com/items?itemName=cueavyqwp.langful)

```
key = value # hi, this is a example
# hi, I am a example, too
... = ...
```

## init

there have `two` ways to init

### by files

```python
import langful
lang = langful.lang()
```

then you can put file at there :

* lang
* * en_us.lang
* * en_us.json
* * zh_cn.lang
* * zh_cn.json
* * ...

or use other directory name and set `langful.lang( "directory name" )`

### by dictionary

```python
import langful
lang = langful.lang( {
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

## function

### replace

```python
lang = langful.lang( {
    "en_us" : {
        "test" : "{}.{}%"
    }
} )
print( lang.replace( "test" , [ 33 , 3 ] ) )
```

### merge

```python
import langful
lang = langful.lang( {
    "en_us" : {
        "hi" : "Hi" ,
        "welcome" : "Welcome"
    } ,
    "zh_cn" : {
        "hi" : "你好"
    }
} )
print( lang.merge( "en_us" , [ "zh_cn" ] ) )
```

# about

[
[github](https://github.com/cueavy/langful)
|
[pypi](https://pypi.org/project/langful)
]
