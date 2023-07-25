"""
# lang
"""

import json
import os

__all__ = [ "to_json" , "to_lang" , "getdefaultlocale" , "lang" ]

def to_json( lang_file : str ) -> dict[ str , str ] :
    from re import split
    ret = {}
    for line in lang_file.split( "\n" ) :
        try :
            key , value = split( "\s=\s" , line.split( "#" )[ 0 ] , 1 )
            ret[ key ] = value
        except ValueError :
            continue
    return ret

def to_lang( dict_file : dict ) -> str :
    ret = ""
    for key , value in dict_file.items() :
        ret += f"{ key } = { value }\n"
    return ret

def getdefaultlocale() -> str :
    """
    getdefaultlocale will deprecated so use this
    """
    from locale import getlocale
    from sys import platform
    if platform == "win32" :
        code = __import__( "_locale" )._getdefaultlocale()[ 0 ]
        if code and code[ : 2 ] == "0x" :
            from locale import windows_locale
            code = windows_locale.get( int( code , 0 ) )
    else :
        code = getlocale()[ 0 ]
    return code.replace( "-" , "_" ).lower()

class lang :

    system_locale = getdefaultlocale()
    __slots__ = [
        "default_locale" ,
        "replace_letter" ,
        "separators" ,
        "json_first" ,
        "use_locale" ,
        "languages" ,
        "lang_dir" ,
        "is_file" ,
        "types"
        ]

    @property
    def locale( self ) -> str :
        for locale in [ self.use_locale , self.system_locale , self.default_locale ] :
            if locale and locale in self.locales :
                return locale
        raise KeyError( f"no such locale '{ self.system_locale }' or '{ self.default_locale }'" )

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

    def __str__( self ) -> str :
        return json.dumps( self.languages , indent = 4 , ensure_ascii = False , separators = self.separators )

    def __len__( self ) -> int :
        return len( self.language )

    def __bool__( self ) -> bool :
        return self.system_locale in self.languages

    def __call__( self ) -> None :
        self.init()

    def __init__( self , lang_dir : str | dict = "lang" , default_locale : str = "en_us" , json_first : bool = True ) -> None :
        """
        lang_dir: lang files dir, if use dict to set that to a dictionary or False
        default_locale: default locale
        json_first: is load json file first
        """
        self.default_locale = default_locale
        self.separators = [ " ," , ": " ]
        self.json_first = json_first
        self.replace_letter = "%"
        self.lang_dir = lang_dir
        self.use_locale = None
        self.is_file = False
        self.languages = {}
        self.types = {}
        self.init()

    def init( self ) :
        if isinstance( self.lang_dir , str ) :
            self.init_file( self.lang_dir )
        elif isinstance( self.lang_dir , dict ) :
            self.init_dict( self.lang_dir )

    def init_file( self , path ) -> None :
        """
        init by a directory
        """
        self.is_file = True
        if not os.path.exists( path ) :
            raise FileNotFoundError( f"can't find '{ os.path.abspath( path ) }'" )
        loads = [ [ ".lang" , ".json" ] , [ ".json" , ".lang" ] ][ self.json_first ]
        for lang_file in os.listdir( path ) :
            name , suffix = os.path.splitext( lang_file )
            if ( suffix in loads ) and ( ( suffix == loads[ 0 ] ) or ( suffix not in self.locales ) ) :
                with open( os.path.join( path , lang_file ) , "r" , encoding = "utf-8" ) as file :
                    if suffix == ".json" :
                        try :
                            data = json.load( file )
                        except json.decoder.JSONDecodeError :
                            raise SyntaxError( "can't to load .json file" )
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
        self.is_file = False
        for key in language.keys() :
            self.types[ key ] = ".json"
        self.languages = language
        self.lang_dir = language

    def to_dict( self ) :
        self.types = { key : ".json" for key in self.types.keys() }
        self.lang_dir = self.languages
        self.is_file = False

    def to_file( self , path ) :
        if not os.path.exists( path ) :
            os.makedirs( path )
        self.lang_dir = path
        self.is_file = True

    def locale_get( self , locale : str = None ) -> str :
        if locale :
            return locale
        else :
            return self.locale

    def locale_set( self , locale : str = None  ) -> None :
        if locale and locale not in self.locales :
            raise KeyError( f"no such locale '{ locale }'" )
        self.use_locale = locale

    def lang_get( self , locale : str ) -> dict[ str , str ] :
        return self.languages[ locale ]

    def lang_set( self , locale : str , value : dict = {} , suffix : str = ".json" ) -> None :
        self.languages[ locale ] = value
        self.types[ locale ] = suffix

    def lang_remove( self , locale : str ) -> None :
        del self.languages[ locale ]
        del self.types[ locale ]

    def lang_merge( self , to : str , locale : str = None , args : str | list[ str ] = [] ) -> None :
        self.lang_set( to , self.merge( locale , args ) )

    def get( self , key : str , locale : str = None ) -> str :
        locale = self.locale_get( locale )
        return self.languages[ locale ][ key ]

    def set( self , key : str , value : str , locale : str = None ) -> None :
        locale = self.locale_get( locale )
        self.languages[ locale ][ key ] = value

    def remove( self , key : str , locale : str = None ) -> None :
        locale = self.locale_get( locale )
        del self.languages[ locale ][ key ]

    def merge( self , locale : str = None , args : list[ str ] = [] ) -> dict[ str , str ] :
        ret = self.lang_get( self.locale_get( locale ) )
        for locale_key in args :
            for key , value in self.lang_get( locale_key ).items() :
                ret[ key ] = value
        return ret

    def save( self ) -> dict[ str , str ] :
        if self.is_file :
            for key , value in self.languages.items() :
                suffix = self.types[ key ]
                with open( os.path.join( self.lang_dir , key + suffix ) , "w" , encoding = "utf-8" ) as file :
                    if suffix == ".json" :
                        json.dump( value , file , indent = 4 , separators = self.separators , ensure_ascii = False )
                    elif suffix == ".lang" :
                        file.write( to_lang( value ) )
        return self.languages

    def replace( self , key : str = None , args : list[ str ] = None , locale : str = None ) -> str :
        replace_letter = self.replace_letter
        locale = self.locale_get( locale )
        index = 0
        ret = ""
        for text in self.get( key , locale ) :
            if text == replace_letter :
                if len( ret ) and ret[ -1 ] == "\\" :
                    ret = ret[ : -1 ] + replace_letter
                else :
                    ret += str( args[ index ] )
                    index += index < len( args ) - 1
            else :
                ret += text
        return ret
