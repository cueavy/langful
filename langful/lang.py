"""
# lang
"""

import json
import os

def to_json( lang_file : str ) -> dict :
    """
    .lang -> .json
    """
    import re
    ret = {}
    for line in lang_file.split( "\n" ) :
        text = re.split( "([^#^=^\\s]+|)(\\s+=\\s+|\\s+=|=\\s+|=|)([^#^\\n]+|)" , line )
        n = 0
        for s in text :
            if "=" in s :
                break
            n += 1
        else :
            continue
        ret[ "".join( text[:n] ) ] = "".join( text[n + 1:] )
    return ret

def to_lang( dict_file : dict ) -> str :
    """
    .json -> .lang
    """
    ret = ""
    for key , value in dict_file.items() :
        ret += f"{ key } = { value }\n"
    return ret

def getdefaultlocale() -> str :
    """
    getdefaultlocale will deprecated so use this
    """
    import locale
    import sys
    if sys.platform == "win32" :
        code = __import__( "_locale" )._getdefaultlocale()[ 0 ]
        if code[ :2 ] == "0x" :
            code = locale.windows_locale[ code ]
    else :
        code = locale.getlocale()[ 0 ]
    return code.replace( "-" , "_" ).lower()

class lang :
    """
    # lang
    """

    def __setitem__( self , key , value ) -> None :
        """
        set
        """
        self.set( key , value )

    def __delitem__( self , key ) -> None :
        """
        remove
        """
        self.remove( key )

    def __getitem__( self , key ) -> str :
        """
        get
        """
        return self.get( key )

    def __call__( self ) -> None :
        """
        init
        """
        self.init()

    def __len__( self ) -> int :
        return len( self.languages )

    def __init__( self , lang_dir : str | dict = "lang" , default_locale : str = "en_us" , json_first : bool = True ) -> None :
        """
        lang_dir: lang files dir, if use dict to set that to a dictionary or False
        default_locale: default locale
        json_first: is load json file first
        """
        self.system_locale = getdefaultlocale()
        self.default_locale = default_locale
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
        files = []
        for i in os.listdir( path ) :
            name , suffix = os.path.splitext( i )
            if ( suffix in loads ) and ( ( suffix == loads[ 0 ] ) or ( name + loads[ 0 ] not in files ) ) :
                files.append( i )
                with open( os.path.join( path , i ) , "r" , encoding = "utf-8" ) as file :
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
        if self.use_locale and self.use_locale in self.locales :
            return self.use_locale
        elif self.system_locale in self.locales :
            return self.system_locale
        elif self.default_locale in self.locales :
            return self.default_locale
        else :
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

    def locale_get( self , locale : str = None ) -> str :
        """
        get locale, usually use in function
        """
        if locale :
            return locale
        else :
            return self.locale

    def replace_letter_get( self , replace_letter : str = None ) -> str :
        """
        get replace letter, usually use in function
        """
        if replace_letter :
            return replace_letter
        else :
            return self.replace_letter

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
        set a new lang
        """
        self.languages[ locale ] = value
        self.types[ locale ] = suffix

    def lang_del( self , locale : str ) -> None :
        """
        del a lang
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

    def save( self , separators : list = [ " ," , ": " ] ) -> None :
        """
        save file when is_file variable is true, else raise the error
        """
        if isinstance( self.lang_dir , str ) :
            for key , value in self.languages.items() :
                suffix = self.types[ key ]
                with open( os.path.join( self.lang_dir , key + suffix ) , "w" , encoding = "utf-8" ) as file :
                    if suffix == ".json" :
                        file.write( json.dumps( value , indent = 4 , separators = separators , ensure_ascii = False ) )
                    elif suffix == ".lang" :
                        file.write( to_lang( value ) )
        return self.languages

    def merge( self , locale : str = None , args : str | list = [] ) -> dict :
        """
        merge
        """
        if isinstance( args , str ) :
            args = [ args ]
        ret = self.lang_get( self.locale_get( locale ) )
        for i in args :
            for key , value in self.lang_get( i ).items() :
                ret[ key ] = value
        return ret

    def replace( self , key : str = None , args : str | list  = None , locale : str = None , replace_letter : str = None ) -> str :
        """
        replace
        """
        replace_letter = self.replace_letter_get( replace_letter )
        locale = self.locale_get( locale )
        text = self.get( key , locale ).split( replace_letter )
        if isinstance( args , str ) :
            args = [ args ]
        ret = ""
        p = 0
        for i in text :
            ret += i
            if ( p + 1 ) < len( text ) :
                if p < len( args ) :
                    ret += str( args[ p ] )
                else :
                    ret += str( args[ -1 ] )
                p += 1
        return ret

    def replace_str( self , text : str , locale : str = None , replace_letter : str = None ) -> str :
        """
        replace by str
        """
        locale = self.locale_get( locale )
        replace_letter = self.replace_letter_get( replace_letter )
        text = text.split( replace_letter )
        ret = ""
        p = 0
        for i in text :
            if p % 2 :
                if i :
                    ret += self.get( i )
                else :
                    ret += replace_letter
            else :
                ret += i
            p += 1
        return ret
