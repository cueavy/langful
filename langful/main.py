from langful.__init__ import *

class lang :

    global os , locale , json

    def __init__( self , lang_dir : str = "lang" , default_lang_file : str = "en_us.json"  ) :
        """
        # langful

        ---

        ## lang object

        lang_dir: Translation file storage directory

        default_lang_file: Default translation file

        ---

        ## lang 对象

        lang_dir: 翻译文件的存放目录

        default_lang_file: 默认使用的翻译文件
        """
        if not os.path.exists( lang_dir ) :
            raise KeyError( "'lang_dir' dir not find" ) # lang文件目录找不到
        if not os.path.exists( os.path.join( lang_dir , default_lang_file ) ) :
            raise KeyError( "'default_lang_file' file not find" )
        lang_file = os.path.join( lang_dir , locale.getdefaultlocale()[0].lower() + ".json" )
        if not os.path.exists( lang_file ) : lang_file = default_lang_file # 若本地化不存在就使用默认指定的语言
        lang_file = os.path.join( lang_dir , lang_file )

        self.lang_dir = lang_dir
        self.default_lang_file = default_lang_file
        self.lang_file = lang_file