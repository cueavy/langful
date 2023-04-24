"""
# lang
"""
import traceback
import locale
import json
import os

from langful.define import *

class lang :

    def __init__( self , lang_dir = "lang" , default_lang : str = "en_us" , file_type : str = JSON , change : str = "%" ) -> None :
        """
        # lang object

        ---

        lang_dir: Translation file storage directory / Translation file dictionary

        default_lang: Default translation

        file_type: 'json' or 'lang'

        change: Specifies what character to use for substitution , default is '%'

        ---

        lang_dir: 翻译文件的存放目录 / 翻译文件字典

        default_lang: 默认使用的翻译

        file_type: 文件后缀 'json' 或 'lang'

        change: 选择用什么符号做替换 默认为'%'

        """

        default_locale = locale.getdefaultlocale()[0].lower() # 默认语言
        self.type = get_type( lang_dir )

        if self.type == FILE :

            file_suffix = f".{file_type}"

            if not os.path.exists( lang_dir ) : # 判断lang文件夹是否存在
                raise KeyError( f"'{lang_dir}' dir not find" )
            if not len( os.listdir(lang_dir) ) :
                raise FileNotFoundError( f"'{lang_dir}' has no file!" ) # lang文件夹里没有语言文件
            if not os.path.exists( os.path.join( lang_dir , default_lang + file_suffix ) ) : # 判断default_lang文件是否存在
                raise KeyError( f"'{default_lang}' not find" )

            lang_file = os.path.join( lang_dir , default_locale + file_suffix )
            file_suffix_len = len( file_suffix )
            lang_file_list = []
            language_dict = {}
            use_locale = default_locale
            if not os.path.exists( lang_file ) : # 若默认语言不存在对应的本地化 那么就选用默认语言文件
                use_locale = default_lang
                lang_file = default_lang + file_suffix

            for filename in os.listdir( lang_dir ): # 尝试加载所有能加载的模块
                if len( filename ) > file_suffix_len and filename[ -file_suffix_len: ] == file_suffix :
                    try :
                        with open( os.path.join( lang_dir , filename ) , encoding = UTF8 ) as file :
                            if file_type == JSON :
                                loaded_lang_file = json.load( file ) # 直接加载JSON文件
                            elif file_type == LANG :
                                loaded_lang_file = {}
                                for i in file.read().split( "\n" ) : # 去换行
                                    if i :
                                        key , value = i.split( "=" ) # 键 = 值
                                        if value and value[0] == " " : # 去空格
                                            value = value[ 1: ]
                                        loaded_lang_file[ join( key.split() ) ] = value
                            else :
                                raise TypeError( f"can't use type '{file_type}'" )
                        language_dict[ filename[ :-file_suffix_len ] ] = loaded_lang_file # 加载文件
                        lang_file_list.append( filename )
                    except Exception as error :
                        print( f"{error}\n" )
                        traceback.print_exc()

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
            #file_type: 'json' or 'lang'
            #file_type: 'json' 或 'lang'
            self.file_type = file_type
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
    def _file_suffix_reload( self ) -> None :
        #file_suffix: Such as '.json' '.lang'
        #file_suffix: 文件后缀 例如 '.json' '.lang'
        if self.type == FILE :
            self.file_suffix = "." + self.file_type
    def _reload( self ) -> None :
        self._lang_str_list_reload()
        self._language_reload()
        self._file_suffix_reload()

    def _lang_str_to_language( self , lang_str ) -> dict :
        if not lang_str :
            lang_str = self.use_locale
        if lang_str in self.lang_str_list :
            return self.language_dict[ lang_str ]
        else :
            raise KeyError( f"lang '{lang_str}' has not find!" )

    def save( self ) -> None :
        """
        # save
        to save all lang file

        ---

        保存所有lang文件
        """
        if self.type == FILE :
            for key , value in self.language_dict.items() :
                try :
                    with open( os.path.join( self.lang_dir , key + self.file_suffix ) , "w+" , encoding = UTF8 ) as file :
                        if self.file_type == JSON :
                            file.write( json.dumps( value , indent = 4 , separators = ( " ," , ": " ) , ensure_ascii = False ) )
                        elif self.file_type == LANG :
                            for i_k , i_v in value.items() :
                                line = f"{i_k} = {i_v}\n"
                                file.write( line )
                except Exception as error :
                    print( f"{error}\n" )
                    traceback.print_exc()
        else :
            raise TypeError( f"{self.type} can't to save" )

    def get( self , key : str , lang_str : str = None ) -> str : # 输入键 获取对应的值
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

    def add( self , lang_str : str , set : dict = {} , change_file : bool = False ) -> None :
        """

        # add a new language

        lang_str: the language's name

        set: the language dictionary

        change_file: modify the file

        ---

        # 添加新语言

        lang_str: 语言名称

        set: 语言字典

        change_file: 是否修改文件

        """
        self.language_dict[ lang_str ] = set
        if lang_str == self.default_locale :
            self.use_locale = lang_str
        if self.type == FILE and change_file :
            self.save()
        self._reload()

    def remove( self , lang_str : str , change_file : bool = False ) -> None :
        """

        # remove a language

        lang_str: the language's name

        change_file: modify the file

        ---

        # 移除语言

        lang_str: 语言名称

        change_file: 是否修改文件

        """
        if lang_str == self.use_locale or lang_str == self.default_lang or lang_str == self.default_locale :
            raise RuntimeError( f"can't remove '{lang_str}' " )
        del self.language_dict[ lang_str ]
        del self.lang_str_list[ self.lang_str_list.index( lang_str ) ]
        if self.type == FILE and change_file :
            self.save()
        self._reload()

    def replace( self , key : str = None , args = None , lang_str : str = None , change : str = None ) -> str :
        """
        # replace

        Replace language dictionary one key with list/string

        用 列表/字符串 替换语言字典中的某个键

        ---

        key: dictionary's key

        args: list

        lang_str: Such as 'zh_cn' or 'en_us' and more

        change: Specifies what character to use for substitution , default is '%'

        ---

        key: 键值

        args: 列表

        lang_str: 例如 'zh_cn' 或 'en_us' 等等

        change: 选择用什么符号做替换 默认为'%'
        """
        if not change :
            change = self.change

        language = self._lang_str_to_language( lang_str )

        if ( not key ) or ( key not in language ) :
            raise KeyError( f"can't use key '{key}'" )

        if not ( isinstance( args , str ) or isinstance( args , list ) ) :
            raise TypeError( f"args can't use '{ type( args ) }' type" )

        text = self.get( key , lang_str ).split( change )
        if len( text ) == 1 :
            text = text[0]
        ret = ""

        for i in range_len( text ) :
            if isinstance( text , str ) :
                ret += text[i]
            else :
                if isinstance( args , list ) :
                    if ( len( text ) - 1 ) > i :
                        if len( args ) > i :
                            ret += text[i] + args[i]
                        else :
                            ret += text[i] + args[-1]
                    else :
                        ret += text[i]
                elif isinstance( args , str ) :
                    if ( len( text ) - 1 ) > i :
                        ret += text[i] + args
                    else :
                        ret += text[i]

        return ret

    def str_replace( self , * args : str , lang_str : str = None , change : str = None ) -> str : # 替换字符串 使用%号
        """
        # str_replace

        Replace string with some one language dictionary

        用某个语言字典替换字符串

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

        i = 0
        ret = ""
        text = join( args ).split( change )
        language = self._lang_str_to_language( lang_str )

        for split_text in text :
            if i % 2 :
                if split_text in language :
                    ret += language[split_text]
                elif not split_text :
                    ret += change
                else :
                    raise KeyError( f"key '{split_text}' has not find!" )
            else :
                ret += split_text
            i += 1

        return ret
