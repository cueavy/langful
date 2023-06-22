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
        i = i.split("#")[0]
        i = "".join( i.split( maxsplit = 2 ) )
        if i :
            k , v = i.split( "=" , 1 )
            ret[ k ] = v
    return ret

def json_to_lang( dict_file : dict ) -> str :
    """
    .json -> .lang
    """
    ret = ""
    for k , v in dict_file.items() :
        if not ( isinstance( v , int ) or isinstance( v , str ) ) :
            raise TypeError( f"can't use type '{ type( v ) }'" )
        ret += f"{ k } = { v }\n"
    return ret

class lang :
    """
    # lang
    """

    def __init__( self , lang_dir : str  |  bool = "lang" , default_locale : str = "en_us" ) -> None :
        """
        lang_dir: lang files dir, if use dict to set that False
        default_locale: default locale
        """
        system_locale = self.get_system_locale
        self.default_locale = default_locale
        self.system_locale = system_locale
        self.replace_letter = "%"
        self.lang_dir = lang_dir
        self.is_file = False
        self.languages = {}
        self.locales = []
        self.types = {}
        self.init()

    def init( self ) -> None :
        """
        # init
        """
        path = self.lang_dir
        if not isinstance( path , str ) :
            return
        if not os.path.exists( path ) :
            raise FileNotFoundError( f"can't find '{ os.path.abspath( path ) }'" )
        self.is_file = True
        files = []
        for i in os.listdir( path ) :
            name , suffix = os.path.splitext( i )
            if ( suffix == ".json" ) or ( name + ".json" not in files ) :
                files.append( i )
                with open( os.path.join( path , i ) , encoding = "utf-8" ) as file :
                    if suffix == ".json" :
                        data = json.load( file )
                    elif suffix == ".lang" :
                        data = lang_to_json( file.read() )
                    else :
                        continue
                self.locales.append( name )
                self.languages[ name ] = data
                self.types[ name ] = suffix

    def init_dict( self , language : dict ) -> None :
        """
        init by a dictionary, but cant't to save
        """
        if self.is_file :
            raise TypeError( "can't init by a dictionary, because it's init by a dir" )
        for k in language.keys() :
            self.types[ k ] = ".json"
            self.locales.append( k )
        self.languages = language

    @property
    def get_system_locale( self ) -> str :
        """
        get system locale
        """
        return getdefaultlocale()[0].lower() # 系统语言

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
    def type( self ) -> str :
        """
        get type, '.json' or '.lang'
        """
        return self.types[ self.locale ]

    def set_locale( self , locale : str = None  ) -> None :
        """
        set/reset locale
        """
        if locale != None :
            self.system_locale = locale
        else :
            self.system_locale = self.get_system_locale

    def get( self , key : str | int , locale : str = None ) -> str :
        """
        get
        """
        if not locale :
            locale = self.locale
        return self.languages[ locale ][ key ]

    def set( self , key : str | int , value : str , locale : str = None ) -> None :
        """
        set
        """
        if not locale :
            locale = self.locale
        self.languages[ locale ][ key ] = value

    def remove( self , key : str | int , locale : str = None ) -> None :
        """
        remove
        """
        if not locale :
            locale = self.locale
        del self.languages[ locale ][ key ]

    def save( self ) -> None :
        """
        save file, when is_file is true
        """
        if self.is_file :
            for key , value in self.languages.items() :
                suffix = self.types[ key ]
                print(suffix,value)
                with open( os.path.join( self.lang_dir , key + suffix ) , "w+" , encoding = "utf-8" ) as file :
                    if suffix == ".json" :
                        file.write( json.dumps( value , indent = 4 , separators = ( " ," , ": " ) , ensure_ascii = False ) )
                    elif suffix == ".lang" :
                        file.write( json_to_lang( value ) )
        else :
            raise TypeError( f"can't to save, because it's not a file" )

    def replace( self , key : str = None , args : list = None , locale : str = None , replace_letter : str = None ) -> str :
        """
        replace
        """
        if not replace_letter :
            replace_letter = self.replace_letter
        if not locale :
            locale = self.locale
        text = self.get( key , locale ).split( replace_letter )
        if len( text ) == 1 :
            text = text[0]
        ret = ""
        for i in range( len( text ) ) :
            if ( len( text ) - 1 ) > i :
                if len( args ) > i :
                    ret += text[i] + args[i]
                else :
                    ret += text[i] + args[-1]
            else :
                ret += text[i]
        return ret

    def replace_str( self , text : str , locale : str = None , replace_letter : str = None ) -> str :
        """
        replace_str
        """
        if not replace_letter :
            replace_letter = self.replace_letter
        if not locale :
            locale = self.locale
        i = 0
        ret = ""
        text = text.split( replace_letter )
        language = self.languages[ locale ]
        for split_text in text :
            if i % 2 :
                if split_text in language :
                    ret += language[split_text]
                elif not split_text :
                    ret += replace_letter
                else :
                    raise KeyError( f"key '{split_text}' has not find!" )
            else :
                ret += split_text
            i += 1
        return ret
