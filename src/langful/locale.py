"""
locale
"""

import typing
import locale

__all__ = [ "getdefaultlocale" , "getlocale" , "getencoding" ]

def getdefaultlocale() -> tuple[ str | None | typing.Any , str | None | typing.Any ] :
    try :
        code , encoding = __import__( "_locale" )._getdefaultlocale()
        if code and code[ : 2 ] == "0x" : code = locale.windows_locale[ int( code , 0 ) ]
    except ( ModuleNotFoundError , AttributeError ) :
        code , encoding = locale.getlocale()
    return code , encoding

def getlocale() -> str :
    code = getdefaultlocale()[ 0 ]
    if isinstance( code , str ) : return code.replace( "-" , "_" ).lower()
    else : return ""

def getencoding() -> str :
    encoding = getdefaultlocale()[ 1 ]
    if isinstance( encoding , str ) : return encoding
    else : return ""
