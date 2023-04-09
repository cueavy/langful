FILE = "file"
DICT = "dict"

def get_type( obj ) :
    if isinstance( obj , str ) :
        return FILE
    elif isinstance( obj , dict ) :
        return DICT
    else :
        raise TypeError(f"can't use type {type(obj)}")