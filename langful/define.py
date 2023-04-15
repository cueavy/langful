"""
# define
"""

# type
JSON = "json"
LANG = "lang"

FILE = "file"
DICT = "dict"
# encode/decode
UTF8 = "utf-8"

def get_type( obj ) -> str :
    if isinstance( obj , str ) :
        return FILE
    elif isinstance( obj , dict ) :
        return DICT
    else :
        raise TypeError(f"can't use type { type( obj ) }")