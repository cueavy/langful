import langful
import os

class Test :

    locale = langful.getdefaultlocale()
    file_json = { "zh_cn" : { "test" : "测试" , "..." : "......" } , "en_us" : { "test" : "test" , "..." : "..." } }
    file_lang = { "zh_cn" : "hi = 嗨\n= = 1 + 1" , "en_us" : "hi = hi\n= = 1 + 2" }
    if not os.path.exists( "langs" ) :
        os.mkdir( "langs" )
    lang = langful.lang( file_json )

    def get_file( self ) :
        return self.file_json[ self.locale ] , self.file_lang[ self.locale ]
    def get_lang( self , dict : dict ) :
        return dict[ self.locale ]

    def test( self ) :
        assert self.locale in [ "en_us" , "zh_cn" ]
        assert self.lang.language == self.get_file()[ 0 ]
        assert self.lang.languages == self.file_json
        assert self.lang.lang == self.get_file()[ 0 ]
        assert self.lang.langs == self.file_json

    def test_to_func( self ) :
        assert langful.to_lang( self.get_file()[ 0 ] ) == self.get_lang( { "zh_cn" : "test = 测试\n... = ......" , "en_us" : "test = test\n... = ..." } )
        assert langful.to_json( self.get_file()[ 1 ] ) == self.get_lang( { "zh_cn" : { "hi" : "嗨" , "=" : "1 + 1" } , "en_us" : { "hi" : "hi" , "=" : "1 + 2" } } )
