"""
func
"""

__all__ = [ "format" ]

def format( text : str ) -> str :
    ret : list[ str ] = []
    escape = False
    for char in text :
        if escape :
            ret.append( { "a" : "\a" , "b" : "\b" , "f" : "\f" , "n" : "\n" , "r" : "\r" , "t" : "\t" , "v" : "\v" , "\\" : "\\" }.get( char , f"\\{ char }" ) )
            escape = False
        elif char == "\\" :
            escape = True
        else :
            ret.append( char )
    if escape :
        ret.append( "\\" )
    return "".join( ret )
