# langful

<p align="center">
    <a href="https://pypi.org/project/langful">
        <img alt="PyPI version" src="https://img.shields.io/pypi/v/langful?color=blue">
    </a>
    <a href="https://www.python.org">
        <img alt="Python version" src="https://img.shields.io/badge/python-3.6+-blue">
    </a>
    <a href="https://opensource.org/license/mit/">
        <img alt="license" src="https://img.shields.io/badge/license-MIT-blue">
    </a>
    <a href="https://github.com/cueavyqwp/langful">
        <img alt="Github stars" src="https://img.shields.io/github/stars/cueavyqwp/langful?color=blue">
    </a>
    <a href="https://github.com/cueavyqwp/langful">
        <img alt="Github issues" src="https://img.shields.io/github/issues/cueavyqwp/langful?color=blue">
    </a>
</p>

# install

Use `pip` to install `pip install langful` or `pip3 install langful`

# example(too old)

- test.py
- lang
    - zh_cn.json
    - en_us.json

## zh_cn.json

```json
{
    "hi" : "你好" ,
    "welcome" : "欢迎"
}
```

## en_us.json

```json
{
    "hi" : "Hi" ,
    "welcome" : "Welcome"
}
```

## tset.py

```python
import langful

Text = langful.lang()

print( Text.language_dict )

print( Text.str_replace( "%hi%" , lang_str = "zh_cn" ) )

print( Text.str_replace( "!hi!" , lang_str = "zh_cn" , change = "!" ) )

print( Text.str_replace( "%welcome%" , lang_str = "zh_cn" ) )

print( Text.str_replace( "!welcome!" , lang_str = "zh_cn" , change = "!" ) )

print( Text.str_replace( "%hi%" , lang_str = "en_us" ) )

print( Text.str_replace( "!hi!" , lang_str = "en_us" , change = "!" ) )

print( Text.str_replace( "%welcome%" , lang_str = "en_us" ) )

print( Text.str_replace( "!welcome!" , lang_str = "en_us" , change = "!" ) )

print( )

print( Text.str_replace( "%%" ) )
print( Text.str_replace( "!!" , change = "!" ) )
```

## Output

```python
{'en_us': {'welcome': 'Welcome', 'hi': 'Hi'}, 'zh_cn': {'welcome': '欢迎', 'hi': '你好'}}
你好
你好
欢迎
欢迎
Hi
Hi
Welcome
Welcome

%
!
```

# About

github: https://github.com/cueavyqwp/langful

pypi: https://pypi.org/project/langful

issues: https://github.com/cueavyqwp/langful/issues