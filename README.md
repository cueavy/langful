# langful

⚠ Warning : Under development ⚠

# example

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

print( Text.replace( "%hi%\n%%\n%welcome%" ) )
```

# Output

```python
{'en_us': {'welcome': 'Welcom', 'hi': 'Hi'}, 'zh_cn': {'welcome': '欢迎', 'hi': '你好'}}
Hi
%
Welcome
```

or

```python
{'en_us': {'welcome': 'Welcom', 'hi': 'Hi'}, 'zh_cn': {'welcome': '欢迎', 'hi': '你好'}}
你好
%
欢迎
```

# About

github: https://github.com/cueavyqwp/langful

pypi: https://pypi.org/project/langful

issues: https://github.com/cueavyqwp/langful/issues