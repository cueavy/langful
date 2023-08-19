import typing

__all__ = list[ str ]
__version__ : str

def to_json( text : str ) -> dict[ str , str ] : ...
def to_lang( data : dict ) -> str : ...
def getdefaultlocale() -> str : """getdefaultlocale will deprecated so use this"""

class lang :
    __slots__ : list[ str ]
    locale_use : str | None
    configs : dict[ str ]
    locale_default : str
    locale_system : str
    languages : dict
    path : str
    @property
    def types( self ) -> dict[ set , str ] : ...
    @types.setter
    def types( self , key : str , value : str ) -> None : ...
    @property
    def locale( self ) -> str : ...
    @property
    def locales( self ) -> list[ str ] : ...
    @property
    def language( self ) -> dict[ str , str ] : ...
    @property
    def lang( self ) -> dict[ str , str ] : ...
    @property
    def langs( self ) -> dict[ str , str ] : ...
    def __getitem__( self , key ) -> str : ...
    def __setitem__( self , key , value ) -> None : ...
    def __delitem__( self , key ) -> None : ...
    def __contains__( self , item ) -> bool : ...
    def __enter__( self ) -> lang : ...
    def __iter__( self ) -> typing.Iterable : ...
    def __exit__( self , *args : tuple ) -> None : ...
    def __bool__( self ) -> bool : ...
    def __repr__( self ) -> str : ...
    def __str__( self ) -> str : ...
    def __len__( self ) -> int : ...
    def __init__( self , path : str | dict = "lang" , locale_default : str = "en_us" , json_first : bool = True ) -> None : ...
    def init( self ) -> None : ...
    def init_file( self , path : str ) -> None : """init by a directory"""
    def init_dict( self , languages : dict = None ) -> None : """init by a dictionary, so cant't to save it to the file"""
    def to_dict( self ) -> None : ...
    def to_file( self , path : str ) -> None : ...
    def values( self ) -> list[ str ] : ...
    def items( self ) -> list[ str , dict[ str , str ] ] : ...
    def keys( self ) -> list[ str ] : ...
    def locale_get( self , locale : str = None ) -> str : ...
    def locale_set( self , locale : str = None  ) -> None : ...
    def lang_get( self , locale : str = None ) -> dict[ str , str ] : ...
    def lang_set( self , locale : str = None , value : dict = {} , suffix : str = ".json" ) -> None : ...
    def lang_remove( self , locale : str = None ) -> None : ...
    def lang_pop( self , locale : str = None ) -> dict : ...
    def lang_merge( self , to : str , locale : str = None , args : str | list[ str ] = [] ) -> None : ...
    def get( self , key : str , locale : str = None ) -> str : ...
    def set( self , key : str , value : str , locale : str = None ) -> None : ...
    def remove( self , key : str , locale : str = None ) -> None : ...
    def pop( self , key : str , locale : str = None ) -> str : ...
    def merge( self , locale : str = None , args : list[ str ] = [] ) -> dict[ str , str ] : ...
    def save( self ) -> dict[ str , str ] : ...
    def replace( self , key : str = None , args : list[ str ] | dict[ str , str ] = [] , locale : str = None ) -> str : ...
