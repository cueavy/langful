FILE = "file"
DICT = "dict"

def TheTypeError( obj , message : str = "" ) -> None : raise TypeError(f"{ message }can't use type { type( obj ) }")

def get_type( obj ) -> str :
    if isinstance( obj , str ) :
        return FILE
    elif isinstance( obj , dict ) :
        return DICT
    else :
        TheTypeError( obj )