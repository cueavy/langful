import typing

from langful.default import *
from lib import *

def test() -> None :
    with tmpdir( "lang" ) as path :
        name = os.path.join( path , "tmp.json" )
        data : dict[ str , typing.Any ] = { "a" : "b" , "b" : 1 , "c" : [ None , True , "a" ] }
        JSON().save( data , name )
        assert JSON().load( name ) == data
        name = os.path.join( path , "tmp.lang" )
        data : dict[ str , typing.Any ] = { "a" : "b" , "q" : "a" , "v" : "q" }
        LANG().save( data , name )
        assert LANG().load( name ) == data
