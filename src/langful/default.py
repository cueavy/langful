"""
default loader
"""

import typing
import json

from . import loader as _loader

__all__ = [ "JSON" , "LANG" , "loader" ]

class JSON( _loader.parser ) :

    def __init__( self ) -> None :
        super().__init__()
        self.suffix : str = ".json"
        self.kwargs : dict[ str , typing.Any ] = { "ensure_ascii" : False , "indent" : 4 , "separators" : ( "," , ": " ) }

    def load( self , data : bytes ) -> dict[ str , typing.Any ] :
        return json.loads( data )

    def save( self , data : dict[ str , typing.Any ] ) -> bytes :
        return json.dumps( data , **self.kwargs ).encode()

class LANG( _loader.parser ) :

    def __init__( self ) -> None :
        super().__init__()
        self.suffix : str = ".lang"

    def load( self , data : bytes ) -> dict[ str , typing.Any ] :
        ret : dict[ str , typing.Any ] = {}
        for line in data.decode().splitlines() :
            line = line.partition( "#" )[ 0 ]
            key , sep , value = line.partition( "=" )
            if sep : ret[ key.strip() ] = value.strip()
        return ret

    def save( self , data : dict[ str , typing.Any ] ) -> bytes :
        return "\n".join( f"{ key } = { value }" for key , value in data.items() ).encode()

class loader( _loader.loader ) :

    def __init__( self ) -> None :
        super().__init__()
        self.parsers.append( JSON() )
        self.parsers.append( LANG() )
