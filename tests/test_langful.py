import shutil
import os

from langful.langful import *

def mkdir( path : str ) -> None :
    if os.path.exists( path ) : shutil.rmtree( path )
    os.mkdir( path )

def test() -> None :
    mkdir( "lang" )
    with open( "lang/en_us.lang" , "w" , encoding = "utf-8" ) as fp : fp.write( "a=b\nb=c\np=0" )
    with open( "lang/zh_cn.json" , "w" , encoding = "utf-8" ) as fp : fp.write( """{"a":"test","b":"测试","c":[null,false,3]}""" )
    lang = langful()
    lang.default_locales[-2] = "zh_cn"
    assert len( lang ) == 2
    assert "en_us" in lang
    assert bool( lang )
    lang.merge_all()
    assert len( lang.get_language( "zh_cn" ).items() ) >= len( lang.get_language( "en_us" ).items() )
    with lang : data = lang.languages
    del lang
    lang = langful()
    assert lang.languages == data
    lang.languages = {"a": {"a": "q", "b": 123, "c": [1, 2, True], "d": False}, "b": {"a": "a"}, "c": {"q": "p", "d": "none"}}
    assert lang.merge( "a" , "b" , "c" ) == {"q": "p", "d": "none", "a": "a", "b": 123, "c": [1, 2, True]}
    lang.set_language( { "text" : "the number is {num} \\{ test \\}" } , "test" )
    assert lang.replace( "text" , { "num" : 123 } , locale = "test" ) == "the number is 123 { test }"
    shutil.rmtree( "lang" )
