"""
langful class
"""

import typing
import os

from .locale import getlocale
from . import default

__all__ = [ "langful" ]

class langful :

    @property
    def locale( self ) -> str :
        locales = [ locale for locale in self.default_locales if locale in self.locales ]
        if locales : return locales[ 0 ]
        else : raise KeyError( f"no locales are available" )

    @property
    def locales( self ) -> list[ str ] :
        return list( self.languages.keys() )

    @property
    def language( self ) -> dict[ str , typing.Any ] :
        return self.languages[ self.locale ]

    def __getitem__( self , key : str ) -> str :
        return self.get( key )

    def __setitem__( self , key : str , value : typing.Any ) -> None :
        self.set( key , value )

    def __delitem__( self , key : str ) -> None :
        self.remove( key )

    def __contains__( self , key : str ) -> bool :
        return key in self.languages

    def __enter__( self ) -> "langful" :
        return self

    def __iter__( self ) -> typing.Iterator[ str ] :
        return iter( self.languages )

    def __exit__( self , *_ : tuple[ typing.Any , typing.Any , typing.Any ] ) -> None :
        self.save_all()

    def __bool__( self ) -> bool :
        return self.default_locales[ -2 ] in self.languages

    def __repr__( self ) -> str :
        return str( self )

    def __str__( self ) -> str :
        return str( self.languages )

    def __len__( self ) -> int :
        return len( self.languages )

    def __init__( self , path : str | None = "lang" , locale_default : str = "en_us" , loader : default._loader.loader = default.loader() ) -> None :
        self.default_locales : list[ str ] = [ "" , getlocale() , locale_default ]
        self.languages : dict[ str , dict[ str , typing.Any ] ] = {}
        self.loader : default._loader.loader = loader
        self.types : dict[ str , str ] = {}
        self.path : str = "" if path is None else path
        if path : self.load_all( path )

    def load( self , file : str ) -> bool :
        name = os.path.splitext( os.path.split( file )[ -1 ] )[ 0 ]
        try : data = self.loader.load( file )
        except : return False
        self.types[ name ] = file
        self.languages[ name ] = data
        return True

    def load_all( self , path : str ) -> None :
        if not os.path.exists( path ) : raise FileNotFoundError( "the directory is not exist" )
        elif not os.path.isdir( path ) : raise NotADirectoryError( "the path is exist but not a directory" )
        for file in os.listdir( path ) :
            file = os.path.join( path , file )
            if not os.path.isfile( file ) : continue
            self.load( file )

    def save( self , locale : str | None = None , file : str | None = None , suffix : str | None = None ) -> bool :
        locale = self.get_locale( locale )
        if file is None : file = self.types[ locale ]
        try : self.loader.save( file , self.get_language( locale ) , suffix )
        except : return False
        return True

    def save_all( self , path : str | None = None ) -> None :
        if path is not None :
            if not os.path.exists( path ) : os.makedirs( path )
            elif not os.path.isdir( path ) : raise NotADirectoryError( "the path is exist but not a directory" )
        for locale , file in self.types.items() :
            if path is not None : file = os.path.join( path , os.path.split( file )[ -1 ] )
            self.save( locale , file )

    def values( self ) -> tuple[ dict[ str , typing.Any ] , ... ] :
        return tuple( self.languages.values() )

    def items( self ) -> tuple[ tuple[ str , dict[ str , typing.Any ] ] , ... ] :
        return tuple( zip( self.keys() , self.values() ) )

    def keys( self ) -> tuple[ str , ... ] :
        return tuple( self.languages.keys() )

    def merge( self , locale : str | None = None , *locales : str ) -> dict[ str , typing.Any ] :
        language = self.get_language( locale ).copy()
        for l in locales : language.update( { key : value for key , value in self.get_language( l ).items() } )
        return language

    def merge_all( self , default_locale : str | None = None ) -> None :
        if default_locale is None : default_locale = self.default_locales[ -1 ]
        if default_locale not in self.locales : raise KeyError( "the default locale is not in the locales" )
        locales = self.locales.copy()
        locales.remove( default_locale )
        for locale in locales : self.set_language( self.merge( default_locale , locale ) , locale )

    def get( self , key : str , locale : str | None = None ) -> typing.Any :
        return self.get_language( locale )[ key ]

    def get_language( self , locale : str | None = None ) -> dict[ str , typing.Any ] :
        return self.languages[ self.get_locale( locale ) ]

    def get_type( self , locale : str | None = None ) -> str :
        return self.types[ self.get_locale( locale ) ]

    def get_locale( self , locale : str | None = None ) -> str :
        return self.locale if locale is None else locale

    def set( self , key : str , value : typing.Any , locale : str | None = None ) -> None :
        self.get_language( locale )[ key ] = value

    def set_language( self , data : dict[ str , typing.Any ] = {} , locale : str | None = None , type : str | None = None ) -> None :
        self.languages[ self.get_locale( locale ) ] = data
        if type is not None : self.set_type( type )

    def set_type( self , type : str = ".json" , locale : str | None = None ) -> None :
        self.types[ self.get_locale( locale ) ] = type

    def set_locale( self , locale : str = "" ) -> None :
        self.default_locales[ 0 ] = locale

    def remove( self , key : str , locale : str | None = None ) -> None :
        del self.get_language( locale )[ key ]

    def remove_language( self , locale : str | None = None ) -> None :
        del self.languages[ self.get_locale( locale ) ]
        self.remove_type( locale )

    def remove_type( self , locale : str | None = None ) -> None :
        del self.types[ self.get_locale( locale ) ]

    def remove_locale( self ) -> None :
        self.default_locales[ 0 ] = ""

    def pop( self , key : str , locale : str | None = None ) -> typing.Any :
        ret = self.get( key , locale )
        self.remove( key , locale )
        return ret

    def pop_language( self , locale : str | None = None ) -> dict[ str , typing.Any ] :
        ret = self.get_language( locale )
        self.remove_language( locale )
        return ret

    def pop_type( self , locale : str | None = None ) -> str :
        ret = self.get_type( locale )
        self.remove_type( locale )
        return ret

    def pop_locale( self ) -> str :
        ret = self.get_locale()
        self.remove_locale()
        return ret
