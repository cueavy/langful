"""
loader
"""

import typing
import abc
import os

__all__ = [ "parser" , "loader" ]

class parser :

    def __init__( self ) -> None :
        self.suffix : list[ str ] | str

    @abc.abstractmethod
    def load( self , data : bytes ) -> dict[ str , typing.Any ] : pass

    @abc.abstractmethod
    def save( self , data : dict[ str , typing.Any ] ) -> bytes : pass

class loader :

    def __contains__( self , key : str ) -> bool :
        return key in self.suffixes

    def __getitem__( self , key : str ) -> parser :
        return self.suffixes[ key ]

    @property
    def suffixes( self ) -> dict[ str , parser ] :
        suffixes : dict[ str , parser ] = {}
        for p in self.parsers : suffixes.update( { suffix : p for suffix in ( p.suffix if isinstance( p.suffix , list ) else [ p.suffix ] ) } )
        return suffixes

    def __init__( self ) -> None :
        self.parsers : list[ parser ] = []

    def load( self , file : str , suffix : str | None = None ) -> dict[ str , typing.Any ] :
        if suffix is None : suffix = os.path.splitext( file )[ -1 ]
        if suffix not in self : raise KeyError( f"no parser can load file with '{ suffix }' suffix" )
        if not os.path.exists( file ) : raise FileNotFoundError( "the file is not exist" )
        elif not os.path.isfile( file ) : raise IsADirectoryError( "the path is exist but not a file" )
        with open( file , "rb" ) as fp : return self.suffixes[ suffix ].load( fp.read() )

    def save( self , file : str , data : dict[ str , typing.Any ] , suffix : str | None = None ) -> None :
        if suffix is None : suffix = os.path.splitext( file )[ -1 ]
        if suffix not in self : raise KeyError( f"no parser can load file with '{ suffix }' suffix" )
        with open( file , "wb" ) as fp : fp.write( self.suffixes[ suffix ].save( data ) )
