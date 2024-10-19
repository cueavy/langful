"""
loader
"""

import typing
import abc
import os

__all__ = [ "parser" , "loader" ]

class parser :

    def __init__( self ) -> None :
        self.suffix : tuple[ str ] | str

    @abc.abstractmethod
    def load( self , path : str ) -> dict[ str , typing.Any ] : pass

    @abc.abstractmethod
    def save( self , data : dict[ str , typing.Any ] , path : str ) -> None : pass

class loader :

    def __contains__( self , key : str ) -> bool :
        return key in self.suffixes

    def __getitem__( self , key : str ) -> parser :
        return self.suffixes[ key ]

    @property
    def suffixes( self ) -> dict[ str , parser ] :
        suffixes : dict[ str , parser ] = {}
        for p in self.parsers : suffixes.update( { suffix : p for suffix in ( p.suffix if isinstance( p.suffix , tuple ) else [ p.suffix ] ) } )
        return suffixes

    def __init__( self ) -> None :
        self.parsers : list[ parser ] = []

    def load( self , file : str , suffix : str | None = None ) -> dict[ str , typing.Any ] :
        if suffix is None : suffix = os.path.splitext( file )[ -1 ]
        if suffix not in self : raise KeyError( f"no parser can load file with '{ suffix }' suffix" )
        if not os.path.exists( file ) : raise FileNotFoundError( "the file is not exist" )
        elif not os.path.isfile( file ) : raise IsADirectoryError( "the path is exist but not a file" )
        return self.suffixes[ suffix ].load( file )

    def save( self , file : str , data : dict[ str , typing.Any ] , suffix : str | None = None ) -> None :
        if os.path.exists( file ) and not os.path.isfile( file ) : raise IsADirectoryError( "the path is not a file" )
        if suffix is None : suffix = os.path.splitext( file )[ -1 ]
        if suffix not in self : raise KeyError( f"no parser can load file with '{ suffix }' suffix" )
        self.suffixes[ suffix ].save( data , file )
