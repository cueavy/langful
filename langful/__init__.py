"""
# langful

Help to localization

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
"""

# 'lang' object
from langful.lang import *
# Some function for 'langful'
from langful.function import *
# define
from langful.define import *