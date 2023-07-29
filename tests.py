import langful
import os

def test_getdefaultlocale() :
    if langful.getdefaultlocale() not in [ "en_us" , "zh_cn" ] :
        raise RuntimeError

def test_to_json() :
    if langful.to_json( "test = ok\n= = 1 + 1# hi\n# 233" ) != { "test" : "ok" , "=" : "1 + 1" } :
        raise RuntimeError

def test_to_lang() :
    if langful.to_lang( { "test" : "ok" , "=" : "1 + 1" } ) != "test = ok\n= = 1 + 1" :
        raise RuntimeError

def test_langs() :
    lang = langful.lang( {
        "en_us" : {
            "test" : "test"
        } ,
        "zh_cn" : {
            "test" : "测试"
        }
    } )
    print( lang.languages )
    print( lang.language )
    print( lang.langs )
    print( lang.lang )
