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
        if not os.path.exists( lang_dir ) : # 判断lang文件夹是否存在
            raise KeyError( "'lang_dir' dir not find" )
        
        if not len( os.listdir(lang_dir) ) : raise RuntimeError( "Give's dir has no lang file!" ) # lang文件夹里没有语言文件

        if not os.path.exists( os.path.join( lang_dir , default_lang + ".json" ) ) : # 判断default_lang文件是否存在
            raise KeyError( "'default_lang' file not find" )
        
        default_locale = locale.getdefaultlocale()[0].lower() # 默认语言
        lang_file = os.path.join( lang_dir , default_locale + ".json" )

        use_locale = default_locale
        if not os.path.exists( lang_file ) : # 若默认语言不存在对应的本地化 那么就选用默认语言文件
            use_locale = default_lang
            lang_file = default_lang + ".json"

        lang_file_list = []
        language_dict = {}

        for filename in os.listdir(lang_dir):
            if len( filename ) > 5 and filename[-5:] == ".json" :
                try :
                    with open( os.path.join( lang_dir , filename ) , encoding= "utf-8" ) as file :
                        language_dict[filename[:-5]] = json.load(file)
                    lang_file_list.append( filename )
                except : pass

        #lang_dir: Translation file storage directory
        #lang_dir: 翻译文件的存放目录
        self.lang_dir = lang_dir
        #default_lang: Default translation
        #default_lang: 默认使用的翻译
        self.default_lang = default_lang
        # lang_file: Choose to use's language file
        # lang_file: 选择使用的语言文件
        self.lang_file = lang_file
        # lang_file_list: All can find's language file
        # lang_file_list: 所有能找到的语言文件
        self.lang_file_list = lang_file_list
        # language_dict: Load all can read's language file
        # language_dict: 加载所有可以读取的语言文件
        self.language_dict = language_dict
        # language: Load need's language file
        # language: 加载需要的语言文件
        self.language = language_dict[ use_locale ]
        # default_locale: The default language
        # default_locale:  默认语言
        self.default_locale = default_locale
        # use_locale: The selected language
        # use_locale: 选定的语言
        self.use_locale = use_locale

    def get( self , key:str , language:dict = None ) : # 输入键 获取对应的值
        if not language : language = self.language
        if key in language :
            return language[key]
        else:
            if key in self.language_dict[ self.default_lang ] :
                return language[key]
            else:
                raise KeyError( "Give's value has not in this dictionary!" )

    def set( self , name:str , value:str , language:dict = None ) :
        if not language : language = self.language
        language[ name ] = value

    def replace( self , *args:str , language:dict = None ) :
        if not language : language = self.language
        text = "".join(args)
        i = 0
        Ret = ""
        for I in text.split( "%" ) :
            if i % 2 :
                if I in language :
                    Ret += language[I]
                elif not I :
                    Ret += "%"
                else:
                    raise KeyError( f"Name '{I}' has not in this dictionary!" )
            else :
                Ret += I
            i += 1
        return Ret