"""
# function
"""
from langful.__init__ import *

def if_then( text : str = "" , replace = "" , change : str = "%" , else_replace : str = "" ) -> str :
    """
    # 'if_then' function
    ---
    If the Boolean value of a particular item is true or false

    then replace it for the str or list

    ---
    text: the text
    replace: give str or list for replace the text
    change: Specifies what character to use for substitution , default is '%'
    else_replace: if it was not , then use it to replace
    ---
    如果某个特定项的布尔值为真或假
    
    那么替换为对应的字符串或列表

    ---
    text: 文本
    replace: 给一个字符串或列表 来替换文本
    change: 选择用什么符号做替换 默认为'%'
    else_replace: 如果为否 那么用这个来做替换
    ---
    """
    i , p = 0 , 0
    Ret = ""
    text = "".join( text ).split( change )
    for I in text :
        if i % 2 :
            if not I :
                Ret += change
            elif len( replace ) < p :
                pass # 列表中没数据了 直接跳过
            elif bool( eval( I ) ) :
                if isinstance( replace , list ) : # 传入的是列表
                    Ret += replace[ p ]
                    p += 1
                else : #传入的是字符串
                    Ret += replace
            else :
                Ret += else_replace # 否则就使用 else_replace 变量中的字符串做替换
        else :
            Ret += I
        i += 1
    return Ret

