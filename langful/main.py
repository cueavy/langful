from langful.__init__ import *

class lang :

    global os , locale , json

    def __init__( self , lang_dir : str = "lang" , default_lang : str = "en_us"  ) :
        """
        # langful

        ---

        ## lang object

        lang_dir: Translation file storage directory

        default_lang: Default translation

        ---

        ## lang 对象

        lang_dir: 翻译文件的存放目录

        default_lang: 默认使用的翻译
        """
        if not os.path.exists( lang_dir ) :
            raise KeyError( "'lang_dir' dir not find" ) # lang文件目录找不到
        if not os.path.exists( os.path.join( lang_dir , default_lang + ".json" ) ) :
            raise KeyError( "'default_lang' file not find" )
        default_locale = locale.getdefaultlocale()[0].lower()
        lang_file = os.path.join( lang_dir , default_locale + ".json" )
        use_locale = default_locale
        if not os.path.exists( lang_file ) :
            use_locale = default_lang
            lang_file = default_lang + ".json" # 若本地化不存在就使用默认指定的语言

        lang_file_list = []
        language_dict = {}

        for filename in os.listdir(lang_dir):
            if len( filename ) > 5 and filename[-5:] == ".json" :
                try :
                    with open( os.path.join( lang_dir , filename ) , encoding= "utf-8" ) as file :
                        language_dict[filename[:-5]] = json.load(file)
                    lang_file_list.append( filename )
                except : pass

        self.lang_dir = lang_dir
        self.default_lang = default_lang
        #lang_file: Choose to use's language file
        #lang_file: 选择使用的语言文件
        self.lang_file = lang_file
        #lang_file_list: All can find's language file
        #lang_file_list: 所有能找到的语言文件
        self.lang_file_list = lang_file_list
        self.language_dict = language_dict
        self.language = language_dict[ use_locale ]
        self.default_locale = default_locale
        self.use_locale = use_locale