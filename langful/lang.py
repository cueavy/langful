"""
# lang
"""

import json
import os

__all__ = [ "to_json" , "to_lang" , "getdefaultlocale" , "lang" ]

def to_json( lang_file : str ) -> dict :
    """
    .lang -> .json
    """
    import re
    ret = {}
    for line in lang_file.split( "\n" ) :
        text = re.split( "([^#^=^\\s]+|)(\\s+=\\s+|\\s+=|=\\s+|=|)([^#^\\n]+|)" , line )
        index = 0
        for value in text :
            if "=" in value :
                ret[ "".join( text[ :index ] ) ] = "".join( text[ index + 1 : ] )
                break
            index += 1
    return ret

def to_lang( dict_file : dict ) -> str :
    """
    .json -> .lang
    """
    ret = ""
    for key , value in dict_file.items() :
        ret += f"{ key } = { value }\n"
    return ret

def to_list( args : str | list ) -> list :
    """
    only use it in this file don't add it in __all__ list
    """
    if isinstance( args , list ) :
        return args
    else :
        return [ args ]

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
    """
    # lang
    """

    @property
    def locales( self ) -> list :
        """
        locales
        """
        return list( self.types.keys() )

    @property
    def locale( self ) -> str :
        """
        choose locale
        """
        for locale in [ self.use_locale , self.system_locale , self.default_locale ] :
            if locale and locale in self.locales :
                return locale
        raise KeyError( f"no such locale '{ self.system_locale }' or '{ self.default_locale }'" )

    @property
    def language( self ) -> dict :
        """
        get now language
        """
        return self.lang_get( self.locale )

    @property
    def lang( self ) -> dict :
        """
        same to language function
        """
        return self.language

    @property
    def langs( self ) -> dict :
        """
        same to languages variable
        """
        return self.languages

    @property
    def type( self ) -> str :
        """
        get type, ".json" or ".lang"
        """
        return self.types[ self.locale ]

    def __getitem__( self , key ) -> str :
        """
        get the value in language variable
        """
        return self.get( key )

    def __setitem__( self , key , value ) -> None :
        """
        set the value in languages[ locale ]
        """
        self.set( key , value )

    def __delitem__( self , key ) -> None :
        """
        remove the value in languages[ locale ]
        """
        self.remove( key )

    def __call__( self ) -> None :
        """
        init function
        """
        self.init()

    def __str__( self ) -> str :
        """
        to string
        """
        return json.dumps( self.languages , indent = 4 , ensure_ascii = False , separators = self.separators )

    def __len__( self ) -> int :
        """
        how many item in language variable
        """
        return len( self.language )

    def __bool__( self ) -> bool :
        """
        is system locale in languages dictionary
        """
        return self.system_locale in self.languages

    def __init__( self , lang_dir : str | dict = "lang" , default_locale : str = "en_us" , json_first : bool = True ) -> None :
        """
        lang_dir: lang files dir, if use dict to set that to a dictionary or False
        default_locale: default locale
        json_first: is load json file first
        """
        self.system_locale = getdefaultlocale()
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
        """
        init
        """
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
        """
        set type to dict
        """
        self.types = { key : ".json" for key in self.types.keys() }
        self.lang_dir = self.languages
        self.is_file = False

    def to_file( self , path ) :
        """
        set type to file
        """
        if not os.path.exists( path ) :
            os.makedirs( path )
        self.lang_dir = path
        self.is_file = True

    def locale_get( self , locale : str = None ) -> str :
        """
        get locale, usually use in function
        """
        if locale :
            return locale
        else :
            return self.locale

    def locale_set( self , locale : str = None  ) -> None :
        """
        if give a locale then set that, else reset it
        """
        if locale and locale not in self.locales :
            raise KeyError( f"no such locale '{ locale }'" )
        self.use_locale = locale

    def lang_get( self , locale : str ) -> dict :
        """
        get a lang
        """
        return self.languages[ locale ]

    def lang_set( self , locale : str , value : dict = {} , suffix : str = ".json" ) -> None :
        """
        set a lang
        """
        self.languages[ locale ] = value
        self.types[ locale ] = suffix

    def lang_remove( self , locale : str ) -> None :
        """
        remove a lang
        """
        del self.languages[ locale ]
        del self.types[ locale ]

    def lang_merge( self , to : str , locale : str = None , args : str | list = [] ) -> None :
        """
        merge to a locale
        """
        self.lang_set( to , self.merge( locale , args ) )

    def get( self , key : str , locale : str = None ) -> str :
        """
        get the key by a locale dictionary
        """
        locale = self.locale_get( locale )
        return self.languages[ locale ][ key ]

    def set( self , key : str , value : str , locale : str = None ) -> None :
        """
        set a value by a locale dictionary
        """
        locale = self.locale_get( locale )
        self.languages[ locale ][ key ] = value

    def remove( self , key : str , locale : str = None ) -> None :
        """
        remove a value by a locale dictionary
        """
        locale = self.locale_get( locale )
        del self.languages[ locale ][ key ]

    def merge( self , locale : str = None , args : str | list = [] ) -> dict :
        """
        merge
        """
        args = to_list( args )
        ret = self.lang_get( self.locale_get( locale ) )
        for locale_key in args :
            for key , value in self.lang_get( locale_key ).items() :
                ret[ key ] = value
        return ret

    def save( self ) -> dict :
        """
        save file when is_file variable is true
        """
        if self.is_file :
            for key , value in self.languages.items() :
                suffix = self.types[ key ]
                with open( os.path.join( self.lang_dir , key + suffix ) , "w" , encoding = "utf-8" ) as file :
                    if suffix == ".json" :
                        json.dump( value , file , indent = 4 , separators = self.separators , ensure_ascii = False )
                    elif suffix == ".lang" :
                        file.write( to_lang( value ) )
        return self.languages

    def replace( self , key : str = None , args : str | list  = None , locale : str = None ) -> str :
        """
        replace
        """
        replace_letter = self.replace_letter
        locale = self.locale_get( locale )
        args = to_list( args )
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
