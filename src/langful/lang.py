"""
lang class
"""

import typing
import json

from . import func

__all__ = [ "config" , "langful" ]

class config :
    """
    # config
    - `dump_args` : the args when use `json.dump` or `json.dumps`
    - `fuzzy_match` : fuzzy match the locales
    """

    dump_args : dict[ str , typing.Any ] = { "ensure_ascii" : False , "separators" : ( "," , ": " ) , "indent" : 4 }
    fuzzy_match : bool = False

class langful :
    """
    langful
    """

    @property
    def locale( self ) -> str :
        default_locales = self.default_locales[ : : -1 ]
        if self.configs.fuzzy_match : default_locales = [ part for locale in default_locales for part in ( locale , locale.split( "_" )[ 0 ] ) ]
        default_locales = list( dict.fromkeys( locale for locale in default_locales if locale ) )
        for locale in default_locales :
            if locale in self.locales : return locale
        raise KeyError( f"no locales are available" )

    @property
    def locales( self ) -> list[ str ] :
        return list( self.languages.keys() )

    def __init__( self , path : str = "./lang" , default_locale : str = "en_us" , use_loacle : str = "" ) -> None :
        self.default_locales : list[ str ] = [ default_locale , func.getdefaultlocale() , use_loacle ]
        self.languages : dict[ str , dict[ typing.Any , typing.Any ] ] = {}
        self.configs : config = config()
        self.path : str = path
        if path : self.init()

    def init( self ) -> None :
        pass
