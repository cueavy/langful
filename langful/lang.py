"""
# lang
"""

from . import errors

import json
import os

__all__ = [ "__version__" , "to_json" , "to_lang" , "getdefaultlocale" , "lang" ]
__version__ = "0.43"

def to_json( text : str ) -> dict[ str , str ] :
    from re import split
    ret = {}
    for line in text.split( "\n" ) :
        try :
            ret.update( dict( [ split( "\\s=\\s" , line.split( "#" )[ 0 ] , 1 ) ] ) )
        except ValueError :
            continue
    return ret

def to_lang( data : dict ) -> str :
    return "\n".join( [ ' = '.join( item ) for item in list( data.items() ) ] )

def getdefaultlocale() -> str :
    """
    getdefaultlocale will deprecated so use this
    """
    from locale import getlocale
    from sys import platform
    if platform == "win32" :
        code = __import__( "_locale" )._getdefaultlocale()[ 0 ]
        if code and code[ : 2 ] == "0x" :
            code = __import__( "locale" ).windows_locale.get( int( code , 0 ) )
    else :
        code = getlocale()[ 0 ]
    return code.replace( "-" , "_" ).lower()

class lang :

    locale_system = getdefaultlocale()
    __slots__ = [ "locale_default" , "locale_use" , "languages" , "configs" , "types" , "path" ]

    @property
    def locale( self ) -> str :
        for locale in [ self.locale_use , self.locale_system , self.locale_default ] :
            if locale and locale in self.locales :
                return locale
        raise errors.LocaleError( f"no such locale '{ self.locale_system }' or '{ self.locale_default }'" )

    @property
    def locales( self ) -> list[ str ] :
        return list( self.types.keys() )

    @property
    def language( self ) -> dict[ str , str ] :
        return self.lang_get( self.locale )

    @property
    def lang( self ) -> dict[ str , str ] :
        return self.language

    @property
    def langs( self ) -> dict[ str , str ] :
        return self.languages

    def __getitem__( self , key ) -> str :
        return self.get( key )

    def __setitem__( self , key , value ) -> None :
        self.set( key , value )

    def __delitem__( self , key ) -> None :
        self.remove( key )

    def __contains__( self , item ) -> bool :
        return item in self.languages

    def __enter__( self ) -> dict[ str , str ] :
        return self.languages

    def __iter__( self ) -> tuple[ dict[ str , str ] ] :
        return iter( self.keys() )

    def __exit__( self , *args ) -> None :
        self.save() if all( item is None for item in args ) else ...

    def __bool__( self ) -> bool :
        return self.locale_system in self.languages

    def __repr__( self ) -> str :
        return str( self.languages )

    def __call__( self ) -> None :
        self.init()

    def __str__( self ) -> str :
        return json.dumps( self.languages , indent = 4 , ensure_ascii = False , separators = self.configs[ "separators" ] )

    def __len__( self ) -> int :
        return len( self.language )

    def __init__( self , path : str | dict = "lang" , locale_default : str = "en_us" , json_first : bool = True ) -> None :
        """
        path: lang files dir, if use dict to set that to a dictionary or False
        locale_default: default locale
        load: is load json file first
        """
        self.configs = { "separators" : [ " ," , ": " ] , "load" : json_first , "file" : False }
        self.locale_default = locale_default
        self.locale_use = None
        self.languages = {}
        self.path = path
        self.types = {}
        self.init()

    def config( self , key : str , value : str ) -> None :
        if key in self.configs :
            self.configs[ key ] = value
        else :
            raise errors.ConfigError( f"'{ key }' not in configs" )

    def init( self ) :
        if isinstance( self.path , str ) :
            self.init_file( self.path )
        elif isinstance( self.path , dict ) :
            self.init_dict( self.path )

    def init_file( self , path ) -> None :
        """
        init by a directory
        """
        loads = [ [ ".lang" , ".lang" ] , [ ".json" , ".lang" ] ][ self.configs[ "load" ] ]
        self.configs[ "file" ] = True
        self.languages = {}
        self.path = path
        self.types = {}
        for lang_file in os.listdir( path ) :
            name , suffix = os.path.splitext( lang_file )
            if ( suffix in loads ) and ( ( suffix == loads[ 0 ] ) or ( name not in self.locales ) ) :
                with open( os.path.join( path , lang_file ) , "r" , encoding = "utf-8" ) as file :
                    if suffix == ".json" :
                        try :
                            data = json.load( file )
                        except json.decoder.JSONDecodeError :
                            raise errors.DecodeError( "can't to load .json file" )
                    elif suffix == ".lang" :
                        data = to_json( file.read() )
                    else :
                        continue
                self.languages[ name ] = data
                self.types[ name ] = suffix

    def init_dict( self , language : dict = None ) -> None :
        """
        init by a dictionary, so cant't to save it to the file
        """
        self.types = { key : ".json" for key in language.keys() }
        self.configs[ "file" ] = False
        self.languages = language
        self.path = language

    def to_dict( self ) :
        self.types = { key : ".json" for key in self.languages.keys() }
        self.configs[ "file" ] = False

    def to_file( self , path ) :
        if not os.path.exists( path ) :
            os.makedirs( path )
        self.configs[ "file" ] = True
        self.path = path

    def values( self ) -> tuple[ dict[ str , str ] ] :
        return self.languages.values()

    def items( self ) -> tuple[ str , dict[ str , str ] ] :
        return self.languages.items()

    def keys( self ) -> tuple[ str ] :
        return self.languages.keys()

    def locale_get( self , locale : str = None ) -> str :
        return locale if locale else self.locale

    def locale_set( self , locale : str = None  ) -> None :
        if locale and locale not in self.locales :
            raise errors.LocaleError( f"no such locale '{ locale }'" )
        self.locale_use = locale

    def lang_get( self , locale : str ) -> dict[ str , str ] :
        return self.languages[ self.locale_get( locale ) ]

    def lang_set( self , locale : str , value : dict = {} , suffix : str = ".json" ) -> None :
        locale = self.locale_get( locale )
        self.languages[ locale ] = value
        self.types[ locale ] = suffix

    def lang_remove( self , locale : str ) -> None :
        locale = self.locale_get( locale )
        del self.languages[ locale ]
        del self.types[ locale ]

    def lang_merge( self , to : str , locale : str = None , args : str | list[ str ] = [] ) -> None :
        self.lang_set( to , self.merge( locale , args ) )

    def get( self , key : str , locale : str = None ) -> str :
        return self.languages[ self.locale_get( locale ) ][ key ]

    def set( self , key : str , value : str , locale : str = None ) -> None :
        self.languages[ self.locale_get( locale ) ][ key ] = value

    def remove( self , key : str , locale : str = None ) -> None :
        del self.languages[ self.locale_get( locale ) ][ key ]

    def merge( self , locale : str = None , args : list[ str ] = [] ) -> dict[ str , str ] :
        ret = self.lang_get( locale )
        [ ret.update( self.lang_get( key ) ) for key in args ]
        return ret

    def save( self ) -> dict[ str , str ] :
        if self.configs[ "file" ] :
            for key , value in self.languages.items() :
                suffix = self.types[ key ]
                with open( os.path.join( self.path , key + suffix ) , "w" , encoding = "utf-8" ) as file :
                    if suffix == ".json" :
                        json.dump( value , file , indent = 4 , separators = self.configs[ "separators" ] , ensure_ascii = False )
                    elif suffix == ".lang" :
                        file.write( to_lang( value ) )
        return self.languages

    def replace( self , key : str = None , args : list[ str ] | dict[ str , str ] = [] , locale : str = None ) -> str :
        from re import findall
        text = self.get( key , locale )
        index = 0
        for texts in findall( "{[^{^}]*}" , text ) :
            if isinstance( args , ( list , tuple ) ) :
                if len( args ) :
                    s = args[ index ]
                    index += 1 if index < len( args ) - 1 else 0
                else :
                    continue
            elif isinstance( args , dict ) :
                item = texts[ 1 : -1 ].replace( " " , "" )
                if item in args :
                    s = args[ item ]
                else :
                    continue
            else :
                s = args
            text = text.replace( texts , str( s ) , 1 )
        return text
