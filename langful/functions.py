import langful.__init__

def if_then( args : str = "" , replace_list : list or str = "" , change : str = "%" , else_replace : str = "" ) -> str :
    """
    # 'if_then' function
    ---
    If the Boolean value of a particular item is true or false , then replace it for the str or list
    ---
    args: the str
    replace_list: give str or list for replace the str
    change: Specifies what character to use for substitution , default is '%'
    else_replace: if it was not , then use it to replace
    ---
    如果某个特定项的布尔值为真或假 那么替换为对应的字符串或列表进行替换
    ---
    args: 字符串
    replace_list: 给一个字符串或列表 来替换字符串
    change: 选择用什么符号做替换 默认为'%'
    else_replace: 如果为否 那么用这个来做替换
    ---
    """
    i = 0
    p = 0
    Ret = ""
    text = "".join( args ).split( change )
    for I in text :

        if i % 2 :
            if not I : Ret += change
            elif len( replace_list ) < p : pass # 列表中没数据了 直接跳过
            elif bool( eval( I ) ) :
                if isinstance( replace_list , list ) : # 传入的是列表
                    Ret += replace_list[ p ]
                    p += 1
                else : #传入的是字符串
                    Ret += replace_list
            else : Ret += else_replace # 否则就使用 else_replace 变量中的字符串做替换
        else : Ret += I

        i += 1
    return Ret

