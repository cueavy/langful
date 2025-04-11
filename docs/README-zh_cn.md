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
        <p>[ <a href = "./README.md" >English</a> | 简体中文 ]</p>
    <hr>
</div>

# 关于

这是一个用于国际化（i18n）的简单模块

你只需要将本地化文件放入一个文件夹中,就像这样:

```
- lang
- - en_us.json
- - zh_cn.json
```

```python
import langful

lang = langful( "lang" )

print( lang )

```

语言将根据你的系统语言自动选择

默认的语言代码通过`locale`模块来进行获取,并且遵循[RFC 1766](https://datatracker.ietf.org/doc/html/rfc1766.html)标准

`langful`默认支持三种默认本地化文件,你可以轻松的添加自定义加载器

# 安装

`pip install langful`

# 链接

[
[github](https://github.com/cueavy/langful)
|
[pypi](https://pypi.org/project/langful)
]
