# langful

⚠ Warning : Under development ⚠

# example

```
- test.py
- lang
    - zh_cn.json
    - en_us.json
```

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

print( Text.replace( "%hi%\n%welcome%" ) )
```

# About

github: https://github.com/cueavyqwp/langful

pypi: https://pypi.org/project/langful

issues: https://github.com/cueavyqwp/langful/issues