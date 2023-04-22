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

def join( args : list ) -> str :
    """
    # "".join( )
    """
    return "".join( args )

def range_len( obj ) -> list :
    """
    # range( len( ) )
    """
    return list( range( len( obj ) ) )

def get_type( obj ) -> str :
    """
    # get type
    # 获取类型
    """
    if isinstance( obj , str ) :
        return FILE
    elif isinstance( obj , dict ) :
        return DICT
    else :
        raise TypeError(f"can't use type { type( obj ) }")
