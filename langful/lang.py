import locale
import json
import os

from langful.__init__ import *
from langful.define import *

class lang :

    def __init__( self , lang_dir = "lang" , default_lang : str = "en_us" , file_suffix : str = ".json" , change : str = "%" ) -> None :
        """
        # lang object

        ---

        lang_dir: Translation file storage directory / Translation file dictionary

        default_lang: Default translation

        file_suffix: Such as '.json' or '.lang'

        change: Specifies what character to use for substitution , default is '%'

        ---

        lang_dir: 翻译文件的存放目录 / 翻译文件字典

        default_lang: 默认使用的翻译

        file_suffix: 文件后缀 例如 '.json' '.lang' '.txt' 等等

        change: 选择用什么符号做替换 默认为'%'

        """

        default_locale = locale.getdefaultlocale()[0].lower() # 默认语言
        self.type = get_type( lang_dir )

        if self.type == FILE :

            if not os.path.exists( lang_dir ) : # 判断lang文件夹是否存在
                raise KeyError( f"'{lang_dir}' dir not find" )
            if not len( os.listdir(lang_dir) ) :
                raise FileNotFoundError( f"'{lang_dir}' has no file!" ) # lang文件夹里没有语言文件
            if not os.path.exists( os.path.join( lang_dir , default_lang + file_suffix ) ) : # 判断default_lang文件是否存在
                raise KeyError( f"'{default_lang}' not find" )

            lang_file = os.path.join( lang_dir , default_locale + file_suffix )
            file_suffix_len=len(file_suffix)
            lang_file_list = []
            language_dict = {}
            use_locale = default_locale
            if not os.path.exists( lang_file ) : # 若默认语言不存在对应的本地化 那么就选用默认语言文件
                use_locale = default_lang
                lang_file = default_lang + file_suffix

            for filename in os.listdir(lang_dir): # 尝试加载所有能加载的模块
                if len( filename ) > file_suffix_len and filename[-file_suffix_len:] == file_suffix :
                    try :
                        with open( os.path.join( lang_dir , filename ) , encoding = UTF8 ) as file :
                            language_dict[ filename[ :-file_suffix_len ] ] = json.load( file ) # 加载文件
                        lang_file_list.append( filename )
                    except : pass

        elif self.type == DICT :
            use_locale = default_lang
            if default_lang not in lang_dir :
                raise KeyError( f"'{default_lang}' not find" )
            if default_locale in lang_dir :
                use_locale = default_locale
            language_dict = lang_dir

        #lang_dir: Translation file storage directory
        #lang_dir: 翻译文件的存放目录
        self.lang_dir = lang_dir
        #default_lang: Default translation
        #default_lang: 默认使用的翻译
        self.default_lang = default_lang
        # language_dict: Load all can read's language file
        # language_dict: 加载所有可以读取的语言文件
        self.language_dict = language_dict
        # default_locale: The default language
        # default_locale:  默认语言
        self.default_locale = default_locale
        # use_locale: The selected language
        # use_locale: 选定的语言
        self.use_locale = use_locale
        # change: Specifies what character to use for substitution , default is '%'
        # change: 选择用什么符号做替换 默认为'%'
        self.change = change

        if self.type == FILE :
            #file_suffix: Such as '.json' '.lang'
            #file_suffix: 文件后缀 例如 '.json' '.lang'
            self.file_suffix = file_suffix
            # lang_file: Choose to use's language file
            # lang_file: 选择使用的语言文件
            self.lang_file = lang_file
            # lang_file_list: All can find's language file
            # lang_file_list: 所有能找到的语言文件
            self.lang_file_list = lang_file_list

        self._reload()

    def _lang_str_list_reload( self ) -> None :
        # lang_str_list: All can find's language file's name
        # lang_str_list: 所有能找到的语言文件的名字
        self.lang_str_list = list( self.language_dict.keys() )
    def _language_reload( self ) -> None :
        # language: Load need's language file
        # language: 加载需要的语言文件
        self.language = self.language_dict[ self.use_locale ]
    def _reload( self ) -> None :
        self._lang_str_list_reload()
        self._language_reload()

    def get( self , key:str , lang_str:str = None ) -> str : # 输入键 获取对应的值
        """

        # get

        Get one value in some one dictionary

        在某个字典中获取一个值

        ---

        key: The dictionary's key

        lang_str: Such as 'zh_cn' or 'en_us' and more

        ---

        key: 键值

        lang_str: 例如 'zh_cn' 或 'en_us' 等等

        """
        if not lang_str :
            lang_str = self.use_locale

        if lang_str in self.lang_str_list :
            if key in self.language_dict[ lang_str ] :
                return self.language_dict[ lang_str ] [ key ]
            else :
                raise KeyError( f"key '{key}' has not in dictionary!" )
            
        else :
            raise KeyError( f"lang '{lang_str}' has not find!" )

    def set( self , key : str , value : str , lang_str : str = None ) -> None : # 设置某个键值
        """

        Set one value with one key in some one dictionary

        在某个字典中用一个值来设置一个键

        # set

        ---

        key: The dictionary's key

        value: Need to change's value

        lang_str: Such as 'zh_cn' or 'en_us' and more

        ---

        key: 键值

        value: 需要更改的值

        lang_str: 例如 'zh_cn' 或 'en_us' 等等

        """
        if not lang_str :
            lang_str = self.use_locale

        if lang_str in self.lang_str_list :
            self.language_dict[ lang_str ] [ key ] = value

        else :
            raise KeyError( f"lang '{lang_str}' has not find!" )

    def add( self , lang_str : str , set : dict = {} ) -> None :
        """

        # add a new language

        lang_str: the language's name

        set: the language dictionary

        ps: It can't change the file

        ---

        # 添加新语言

        lang_str: 语言名称

        set: 语言字典

        ps: 它不会影响文件

        """
        self.language_dict[ lang_str ] = set
        if lang_str == self.default_locale :
            self.use_locale = lang_str
        self._reload()

    def remove( self , lang_str : str ) -> None : #todo
        """
        # todo
        """
        if lang_str == self.use_locale or lang_str == self.default_lang or lang_str == self.default_locale :
            raise RuntimeError( f"can't remove '{lang_str}' " )
        del self.language_dict[ lang_str ]
        del self.lang_str_list[ self.lang_str_list.index( lang_str ) ]
        self._reload()

    def replace( self , * args : str , lang_str : str = None , change : str = None ) -> str : # 替换字符串 使用%号
        """

        Replace string with some one dictionary

        用某个字典替换字符串

        # replace

        ---

        key: The dictionary's key

        args: Strings

        lang_str: Such as 'zh_cn' or 'en_us' and more

        change: Specifies what character to use for substitution , default is '%'

        ---

        key: 键值

        args: Strings

        lang_str: 例如 'zh_cn' 或 'en_us' 等等

        change: 选择用什么符号做替换 默认为'%'
        """
        if not change :
            change = self.change

        if not lang_str :
            lang_str = self.use_locale

        if lang_str in self.lang_str_list :
            language = self.language_dict[ lang_str ]

        else :
            raise KeyError( f"lang '{lang_str}' has not find!" )

        i = 0
        Ret = ""
        text = "".join( args ).split( change )

        for I in text :
            if i % 2 :
                if I in language :
                    Ret += language[I]
                elif not I :
                    Ret += change
                else :
                    raise KeyError( f"key '{I}' has not find!" )
            else :
                Ret += I
            i += 1

        return Ret