import langful
import json

def test() :

    assert langful.to_lang( { "k" : "v" , "=" : "= 1 + 2" } ) == "k = v\n= = = 1 + 2"
    assert langful.to_json( """k = v\n= = = 1 + 2""" ) == { "k" : "v" , "=" : "= 1 + 2" }
    assert "_" in langful.getdefaultlocale()

    lang = langful.lang( { "test" : { "k" : "v" } , "en_us" : { "hi" : "Hi" , "..." : "..." } } , "test" )

    assert len( lang ) == 2
    assert lang.locale_default == "test"
    assert "test" and "en_us" in lang.types
    assert list( iter( lang ) ) == list( lang.keys() )

    lang.locale_set( "en_us" )
    lang.lang_set( "a" )
    assert "a" in lang.locales
    for i in [ lang.locale , lang.locale_get() ] :
        assert i == "en_us"
    lang.locale_set( "test" )
    lang.lang_remove( "a" )
    assert lang.locale_use == "test"
    assert "a" not in lang.locales

    for i in [ lang.language , lang.lang , lang.lang_get() ] :
        assert i == { "k" : "v" }
    for i in [ lang.languages , lang.langs ] :
        assert "test" and "en_us" in i

    lang.lang_set( "test" )
    assert lang.lang == {}

    lang.set( "k" , "v" )
    lang.set( "test" , "a{a a}.{b}%{}a" )
    lang.lang_merge( "a" , "test" , [ "en_us" ] )
    assert "k" in lang.lang and lang.lang[ "k" ] == "v"
    assert lang.get( "k" ) == "v"
    assert lang.replace( "test" , 3 ) == "a3.3%3a"
    assert lang.replace( "test" , "3" ) == "a3.3%3a"
    assert lang.replace( "test" , [ 3 ] ) == "a3.3%3a"
    assert lang.replace( "test" , [ 33 , 3 , 4 ] ) == "a33.3%4a"
    assert lang.replace( "test" , { "aa" : 33 , "b" : 3 , "" : 4 } ) == "a33.3%4a"
    for i in [ lang.lang_get( "a" ) , lang.merge( "test" , [ "en_us" ] ) ] :
        assert i == { "k" : "v" , "hi" : "Hi" , "..." : "..." , "test" : "a{a a}.{b}%{}a" }
    lang.remove( "..." )
    assert "..." not in lang.lang
    lang.remove( "test" )
    lang.lang_remove( "a" )
    lang.lang_set( "test" , { "k" : "v" } )
    assert json.loads( repr( lang ) ) == json.loads( str( lang ) )

    lang.to_file( "langs" )
    lang.save()

    with lang as l :
        assert l == lang
    del lang

    lang = langful.lang( "langs" , "test" )
    lang.to_dict()
    assert not lang.configs[ "file" ]
    lang.pop( "k" )
    lang.lang_pop( "test" )
