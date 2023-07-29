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
[en_us](./README.md)
|
zh_cn
]

---

</div>

# 安装

`pip3 install langful` 或 `pip install langful`

# 开始

## 翻译文件

> 注: `langful` 默认先加载 `.json` 文件
>
> 或者设置为 `langful.lang( json_first = False )`

.json

```json
{
    "键": "值" ,
    "..." : "..."
}
```

.lang

> 若需要高亮 请安装 `vscode-langful` :
[GitHub](https://github.com/cueavy/vscode-langful)
[VSCode](https://marketplace.visualstudio.com/items?itemName=cueavyqwp.langful)

```
键 = 值 # 嗨, 这是个示例
# 嗨, 这也是个示例
... = ...
```

## 初始化

共有 `两种` 方式进行初始化

### 通过文件

```python
import langful
lang = langful.lang()
```

然后可以将文件放在 :

* lang
* * en_us.lang
* * en_us.json
* * zh_cn.lang
* * zh_cn.json
* * ...

或者设置为别的目录 并设置 `langful.lang( "目录名称" )`

### 通过字典

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

## 函数

### 替换

```python
lang = langful.lang( {
    "en_us" : {
        "test" : "%.%\%"
    }
} )
print( lang.replace( "test" , [ 33 , 3 ] ) )
```

### 合并

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

# 关于

[
[github](https://github.com/cueavy/langful)
|
[pypi](https://pypi.org/project/langful)
]
