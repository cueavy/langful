"""
lang
"""

import json
import os
import re

__all__ = [ "__version__" , "to_json" , "to_lang" , "getdefaultlocale" , "lang" ]
__version__ = "0.49"

def to_json( text : str ) -> dict[ str , str ] :
    ret = {}
    for line in text.split( "\n" ) :
        try :
            ret.update( dict( [ re.split( "\\s=\\s" , line.split( "#" )[ 0 ] , 1 ) ] ) )
        except ValueError :
            continue
    return ret

def to_lang( data : dict ) -> str :
    return "\n".join( [ " = ".join( item ) for item in data.items() ] )

def getdefaultlocale() -> str :
    """
    getdefaultlocale will deprecated so use this
    """
    from locale import getlocale
    from sys import platform
    if platform == "win32" :
        code = __import__( "_locale" )._getdefaultlocale()[ 0 ]
        if code and code[ : 2 ] == "0x" :
            code = __import__( "locale" ).windows_locale[ int( code , 0 ) ]
    else :
        code = getlocale()[ 0 ]
    return code.replace( "-" , "_" ).lower()

class lang :

    locale_system = getdefaultlocale()
    __slots__ = [ "locale_default" , "locale_use" , "languages" , "configs" , "path" ]

    @property
    def types( self ) -> dict[ set , str ] :
        types = { key : value for key , value in self.configs[ "type" ].items() if key in self.languages }
        types.update( { key : ".json" for key in self.languages.keys() if key not in types } )
        self.configs[ "type" ] = types
        return types

    @types.setter
    def types( self , key : str , value : str ) -> None :
        self.configs[ "type" ][ key ] = value
        self.types

    @types.deleter
    def types( self ) -> None :
        self.configs[ "type" ] = {}

    @property
    def locale( self ) -> str :
        for locale in self.locale_use , self.locale_system , self.locale_default :
            if locale and locale in self.locales :
                return locale
        raise KeyError( f"no such locale '{ self.locale_system }' or '{ self.locale_default }'" )

    @property
    def locales( self ) -> list[ str ] :
        return list( self.languages.keys() )

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

    def __enter__( self ) :
        return self

    def __iter__( self ) -> tuple[ dict[ str , str ] ] :
        return iter( self.languages )

    def __exit__( self , *args ) -> None :
        self.save()

    def __bool__( self ) -> bool :
        return self.locale_system in self.languages

    def __repr__( self ) -> str :
        return json.dumps( self.languages , ensure_ascii = False )

    def __call__( self ) -> None :
        self.init()

    def __str__( self ) -> str :
        return repr( self )

    def __len__( self ) -> int :
        return len( self.languages )

    def __init__( self , path : str | dict = "lang" , locale_default : str = "en_us" , json_first : bool = True ) -> None :
        self.configs = { "separators" : [ " ," , ": " ] , "load" : json_first , "file" : False , "type" : {} }
        self.locale_default = locale_default
        self.locale_use = None
        self.languages = {}
        self.path = path
        self.init()

    def init( self ) -> None :
        del self.types
        self.languages = {}
        if isinstance( self.path , str ) :
            self.init_file( self.path )
        elif isinstance( self.path , dict ) :
            self.init_dict( self.path )

    def init_file( self , path : str ) -> None :
        """
        init by a directory
        """
        loads = [ [ ".lang" , ".lang" ] , [ ".json" , ".lang" ] ][ self.configs[ "load" ] ]
        self.configs[ "file" ] = True
        self.path = path
        for lang_file in os.listdir( path ) :
            name , suffix = os.path.splitext( lang_file )
            if ( suffix in loads ) and ( ( suffix == loads[ 0 ] ) or ( name not in self.locales ) ) :
                with open( os.path.join( path , lang_file ) , "r" , encoding = "utf-8" ) as file :
                    if suffix == ".json" :
                        try :
                            data = json.load( file )
                        except json.decoder.JSONDecodeError :
                            continue
                    elif suffix == ".lang" :
                        data = to_json( file.read() )
                    else :
                        continue
                self.lang_set( name , data , suffix )

    def init_dict( self , languages : dict = None ) -> None :
        """
        init by a dictionary, so cant't to save it to the file
        """
        self.configs[ "file" ] = False
        self.languages = languages

    def to_dict( self ) -> None :
        self.init_dict( self.languages )

    def to_file( self , path : str ) -> None :
        os.makedirs( path ) if not os.path.exists( path ) else ...
        self.configs[ "file" ] = True
        self.path = path

    def values( self ) -> list[ dict[ str , str ] ] :
        return list( self.languages.values() )

    def items( self ) -> list[ str , dict[ str , str ] ] :
        return list( self.languages.items() )

    def keys( self ) -> list[ str ] :
        return list( self.languages.keys() )

    def locale_get( self , locale : str = None ) -> str :
        return locale if locale else self.locale

    def locale_set( self , locale : str = None  ) -> None :
        if locale and locale not in self.locales :
            raise KeyError( f"no such locale '{ locale }'" )
        self.locale_use = locale

    def lang_get( self , locale : str = None ) -> dict[ str , str ] :
        return self.languages[ self.locale_get( locale ) ]

    def lang_set( self , locale : str = None , value : dict = {} , suffix : str = ".json" ) -> None :
        locale = self.locale_get( locale )
        self.languages[ locale ] = value
        self.types[ locale ] = suffix

    def lang_remove( self , locale : str = None ) -> None :
        locale = self.locale_get( locale )
        del self.languages[ locale ]

    def lang_pop( self , locale : str = None ) -> dict :
        return self.languages.pop( self.locale_get( locale ) )

    def lang_merge( self , to : str , locale : str = None , args : str | list[ str ] = [] ) -> None :
        self.lang_set( to , self.merge( locale , args ) )

    def get( self , key : str , locale : str = None ) -> str :
        return self.languages[ self.locale_get( locale ) ][ key ]

    def set( self , key : str , value : str , locale : str = None ) -> None :
        self.languages[ self.locale_get( locale ) ][ key ] = value

    def remove( self , key : str , locale : str = None ) -> None :
        del self.languages[ self.locale_get( locale ) ][ key ]

    def pop( self , key : str , locale : str = None ) -> str :
        return self.languages[ self.locale_get( locale ) ].pop( key )

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
        text = self.get( key , locale )
        index = 0
        for texts in re.findall( "{[^{^}]*}" , text ) :
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
