"""
lang
"""

import json
import os
import re

__all__ = [ "to_json" , "to_lang" , "getdefaultlocale" , "lang" ]

def to_json( data : str ) -> dict :
    ret = {}
    for line in data.split( "\n" ) :
        try : ret.update( dict( [ re.split( "\\s*=\\s*" , line.split( "#" )[ 0 ] , 1 ) ] ) )
        except ValueError : continue
    return ret

def to_lang( data : dict ) -> str :
    return "\n".join( f"{ key } = { value }" for key , value in data.items() )

def getdefaultlocale() -> str :
    """
    getdefaultlocale will deprecated so use this
    """
    import locale
    try :
        code = __import__( "_locale" )._getdefaultlocale()[ 0 ]
    except ( ModuleNotFoundError , AttributeError ) :
        code = str( locale.getlocale()[ 0 ] )
    if os.name == "nt" and code and code[ : 2 ] == "0x" :
        code = locale.windows_locale[ int( code , 0 ) ]
    return code.replace( "-" , "_" ).lower()

class lang :

    __slots__ = [ "locale_defaults" , "languages" , "configs" , "path" ]

    @property
    def locale( self ) -> str :
        for locale in [ str( locale ) for locale in self.locale_defaults if locale in self.locales ] : return str( locale )
        raise KeyError( f"no such locales can be use" )

    @property
    def locales( self ) -> list[ str ] :
        return list( self.languages.keys() )

    @property
    def language( self ) -> dict :
        return self.lang_get( self.locale )

    @property
    def lang( self ) -> dict :
        return self.language

    @property
    def langs( self ) -> dict :
        return self.languages

    def __getitem__( self , key ) -> str :
        return self.get( key )

    def __setitem__( self , key , value ) -> None :
        self.set( key , value )

    def __delitem__( self , key ) -> None :
        self.remove( key )

    def __contains__( self , item ) -> bool :
        return item in self.languages

    def __enter__( self ) -> "lang" :
        return self

    def __iter__( self ) -> ... :
        return iter( self.languages )

    def __exit__( self , *args ) -> None :
        self.save()

    def __bool__( self ) -> bool :
        try : return bool( self.locale )
        except KeyError : return False

    def __repr__( self ) -> str :
        return json.dumps( self.languages , ensure_ascii = False )

    def __str__( self ) -> str :
        return repr( self )

    def __len__( self ) -> int :
        return len( self.languages )

    def __init__( self , path : str | dict | None = "lang" , locale_default : str = "en_us" , json_first : bool = True ) -> None :
        self.configs = { "separators" : [ " ," , ": " ] , "load" : json_first , "file" : False }
        self.locale_defaults = [ "" , getdefaultlocale() , locale_default ]
        self.languages = {}
        self.path = path
        self.init()

    def init( self ) -> None :
        self.languages = {}
        if isinstance( self.path , str ) : self.init_file( self.path )
        elif isinstance( self.path , dict ) : self.init_dict( self.path )

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
                        try : data = json.load( file )
                        except json.decoder.JSONDecodeError : continue
                    elif suffix == ".lang" : data = to_json( file.read() )
                    else : continue
                self.lang_set( name , data , suffix )

    def init_dict( self , languages : dict = {} ) -> None :
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

    def values( self ) -> list[ dict ] :
        return list( self.languages.values() )

    def items( self ) -> list[ tuple ] :
        return list( self.languages.items() )

    def keys( self ) -> list[ str ] :
        return list( self.languages.keys() )

    def locale_get( self , locale : str = "" ) -> str :
        return locale if locale else self.locale

    def locale_set( self , locale : str = "" ) -> None :
        self.locale_defaults[ 0 ] = locale

    def lang_get( self , locale : str = "" ) -> dict :
        return self.languages[ self.locale_get( locale ) ]

    def lang_set( self , locale : str = "" , value : dict = {} , suffix : str = ".json" ) -> None :
        self.languages[ self.locale_get( locale ) ] = value

    def lang_remove( self , locale : str = "" ) -> None :
        del self.languages[ self.locale_get( locale ) ]

    def lang_pop( self , locale : str = "" ) -> dict :
        return self.languages.pop( self.locale_get( locale ) )

    def lang_merge( self , to : str , locale : str = "" , args : list[ str ] = [] ) -> None :
        self.lang_set( to , self.merge( locale , args ) )

    def get( self , key , locale : str = "" ) -> str :
        return self.languages[ self.locale_get( locale ) ][ key ]

    def set( self , key , value : str , locale : str = "" ) -> None :
        self.languages[ self.locale_get( locale ) ][ key ] = value

    def remove( self , key , locale : str = "" ) -> None :
        del self.languages[ self.locale_get( locale ) ][ key ]

    def pop( self , key , locale : str = "" ) -> str :
        return self.languages[ self.locale_get( locale ) ].pop( key )

    def merge( self , locale : str = "" , args : list[ str ] = [] ) -> dict :
        ret = self.lang_get( locale )
        [ ret.update( self.lang_get( key ) ) for key in args ]
        return ret

    def save( self ) -> None :
        # if self.configs[ "file" ] :
        #     for key , value in self.languages.items() :
        #         suffix = self.types[ key ]
        #     with open( os.path.join( self.path , key + suffix ) , "w" , encoding = "utf-8" ) as file :
        #         if suffix == ".json" :
        #             json.dump( value , file , indent = 4 , separators = self.configs[ "separators" ] , ensure_ascii = False )
        #         elif suffix == ".lang" :
        #             file.write( to_lang( value ) )
        pass
