import shutil
import os

from langful.default import *

def test() -> None :
    data = b"""{\n    "a": "b",\n    "b": 1,\n    "c": [\n        null,\n        true,\n        "a"\n    ]\n}"""
    dict = JSON().load( data )
    assert dict == { "a" : "b" , "b" : 1 , "c" : [ None , True , "a" ] }
    assert JSON().save( dict ) == data
    data = b"a = b\nq = a\nv = q"
    dict = LANG().load( data )
    assert dict == { "a" : "b" , "q" : "a" , "v" : "q" }
    assert LANG().save( dict ) == data
