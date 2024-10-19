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
        self.suffix = ".json"
        self.kwargs : dict[ str , typing.Any ] = { "ensure_ascii" : False , "indent" : 4 , "separators" : ( "," , ": " ) }

    def load( self , path : str ) -> dict[ str , typing.Any ] :
        with open( path , "rb" ) as fp :
            return json.load( fp )

    def save( self , data : dict[ str , typing.Any ] , path : str ) -> None :
        with open( path , "w" , encoding = "utf-8" ) as fp :
            json.dump( data , fp , **self.kwargs )

class LANG( _loader.parser ) :

    def __init__( self ) -> None :
        super().__init__()
        self.suffix = ".lang"

    def load( self , path : str ) -> dict[ str , typing.Any ] :
        ret : dict[ str , typing.Any ] = {}
        with open( path , "r" , encoding = "utf-8" ) as fp :
            for line in fp.readlines() :
                line = line.partition( "#" )[ 0 ]
                key , sep , value = line.partition( "=" )
                if sep : ret[ key.strip() ] = value.strip()
        return ret

    def save( self , data : dict[ str , typing.Any ] , path : str ) -> None :
        with open( path , "w" , encoding = "utf-8" ) as fp :
            for key , value in data.items() :
                fp.write( f"{ key } = { value }\n" )

class loader( _loader.loader ) :

    def __init__( self ) -> None :
        super().__init__()
        self.parsers.append( JSON() )
        self.parsers.append( LANG() )
