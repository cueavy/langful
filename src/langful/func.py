"""
functions
"""

import typing
import locale
import re

__all__ = [ "to_json" , "to_lang" , "getdefaultlocale" ]

def to_json( data : str ) -> dict[ typing.Any , typing.Any ] :
    ret : dict[ typing.Any , typing.Any ] = {}
    for line in data.split( "\n" ) :
        splits : list[str] = re.split( "\\s*=\\s*" , line.split( "#" )[ 0 ] , 1 )
        if len( splits ) == 2 : ret[ splits[ 0 ] ] = splits[ -1 ]
    return ret

def to_lang( data : dict[ typing.Any , typing.Any ] ) -> str :
    return "\n".join( f"{ key } = { value }" for key , value in data.items() )

def getdefaultlocale() -> str :
    try :
        code = __import__( "_locale" )._getdefaultlocale()[ 0 ]
        if code[ : 2 ] == "0x" : code = locale.windows_locale[ int( code , 0 ) ]
    except ( ModuleNotFoundError , AttributeError ) :
        code = locale.getlocale()[ 0 ]
    return str( code ).replace( "-" , "_" ).lower()
