"""
# lang
"""
from locale import getdefaultlocale
import json
import os

def lang_to_json( lang_file : str ) -> dict :
    """
    .lang -> .json
    """
    ret = {}
    for i in lang_file.split( "\n" ) :
        text = i.split("#")[0]
        line = "".join( text.split( maxsplit = 2 ) )
        if line :
            key_value = i.split( "=" , 1 )
            if len( key_value ) == 2 :
                key , value = i.split( "=" , 1 )
            else :
                raise SyntaxError( "can't to read .lang file" )
            ret[ key ] = value
    return ret

def json_to_lang( dict_file : dict ) -> str :
    """
    .json -> .lang
    """
    ret = ""
    for key , value in dict_file.items() :
        if not ( isinstance( value , int ) or isinstance( value , str ) ) :
            raise TypeError( f"can't use type '{ type( value ) }'" )
        ret += f"{ key } = { value }\n"
    return ret

class lang :
    """
    # lang
    """

    def __setitem__( self , key , value ) -> None :
        self.set( key , value )

    def __delitem__( self , key ) -> None :
        self.remove( key )

    def __getitem__( self , key ) -> str :
        return self.get( key )

    def __call__( self ) -> None :
        self.init()

    def __len__( self ) -> int :
        return len( self.languages )

    def __init__( self , lang_dir : str | dict | bool = "lang" , default_locale : str = "en_us" , json_first : bool = True ) -> None :
        """
        lang_dir: lang files dir, if use dict to set that to a dictionary or False
        default_locale: default locale
        json_first: is load json file first
        """
        system_locale = self.system_locale_get()
        self.default_locale = default_locale
        self.system_locale = system_locale
        self.json_first = json_first
        self.replace_letter = "%"
        self.lang_dir = lang_dir
        self.is_file = False
        self.languages = {}
        self.types = {}
        if isinstance( lang_dir , str ) :
            self.init()
        elif isinstance( lang_dir , dict ) :
            self.init_dict( lang_dir )

    def init( self ) -> None :
        """
        init by a directory
        """
        path = self.lang_dir
        self.is_file = True
        if not isinstance( self.json_first , bool ) :
            self.json_first = True
        if self.json_first :
            loads = [ ".json" , ".lang" ]
        else :
            loads = [ ".lang" , ".json" ]
        if self.is_file :
            if not os.path.exists( path ) :
                raise FileNotFoundError( f"can't find '{ os.path.abspath( path ) }'" )
            files = []
            for i in os.listdir( path ) :
                name , suffix = os.path.splitext( i )
                if ( suffix in loads ) and ( ( suffix == loads[0] ) or ( name + loads[0] not in files ) ) :
                    files.append( i )
                    with open( os.path.join( path , i ) , encoding = "utf-8" ) as file :
                        if suffix == ".json" :
                            try :
                                data = json.load( file )
                            except json.decoder.JSONDecodeError :
                                raise SyntaxError( "can't to load .json file" )
                        elif suffix == ".lang" :
                            data = lang_to_json( file.read() )
                        else :
                            continue
                    self.languages[ name ] = data
                    self.types[ name ] = suffix

    def init_dict( self , language : dict ) -> None :
        """
        init by a dictionary, so cant't to save it to the file
        """
        if self.is_file :
            raise TypeError( "can't init by a dictionary, because it's init by a dir" )
        for value in language.values() :
            if not isinstance( value , dict ) :
                raise TypeError( f"can't use type '{ type( value ) }'" )
        for key in language.keys() :
            self.types[ key ] = ".json"
        self.languages = language

    def system_locale_get( self ) -> str :
        """
        get system locale
        """
        return getdefaultlocale()[0].lower()

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
        if self.system_locale in self.locales :
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
        return self.languages[ self.locale ]

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
        if locale != None :
            self.system_locale = locale
        else :
            self.system_locale = self.system_locale_get()

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

    def get( self , key : str | int , locale : str = None ) -> str :
        """
        get the key by a locale dictionary
        """
        locale = self.locale_get( locale )
        return self.languages[ locale ][ key ]

    def set( self , key : str | int , value : str , locale : str = None ) -> None :
        """
        set a value by a locale dictionary
        """
        locale = self.locale_get( locale )
        self.languages[ locale ][ key ] = value

    def remove( self , key : str | int , locale : str = None ) -> None :
        """
        remove a value by a locale dictionary
        """
        locale = self.locale_get( locale )
        del self.languages[ locale ][ key ]

    def save( self ) -> None :
        """
        save file when is_file variable is true, else raise the error
        """
        if self.is_file :
            for key , value in self.languages.items() :
                suffix = self.types[ key ]
                with open( os.path.join( self.lang_dir , key , suffix ) , "w" , encoding = "utf-8" ) as file :
                    if suffix == ".json" :
                        file.write( json.dumps( value , indent = 4 , separators = ( " ," , ": " ) , ensure_ascii = False ) )
                    elif suffix == ".lang" :
                        file.write( json_to_lang( value ) )
        else :
            raise TypeError( "can't to save, because it's not a file" )

    def save_dict( self ) -> dict :
        """
        save dict. in fact, it just return the "languages" variable
        """
        if not self.is_file :
            return self.languages
        else :
            raise TypeError( "can't to save, because it's not a dict" )

    def replace( self , key : str = None , args : list | str = None , locale : str = None , replace_letter : str = None ) -> str :
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
