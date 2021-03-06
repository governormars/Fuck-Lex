#!/usr/bin/python3
# -*-coding=utf-8
import re
import string

keywords = {}
signlist = {}

# 关键字部分
keywords['main'] = 1
keywords['if'] = 2
keywords['then'] = 3
keywords['while'] = 4
keywords['do'] = 5
keywords['static'] = 6
keywords['default'] = 39
keywords['int'] = 7
keywords['double'] = 8
keywords['struct'] = 9
keywords['break'] = 10
keywords['else'] = 11
keywords['long'] = 12
keywords['switch'] = 13
keywords['case'] = 14
keywords['typedef'] = 15
keywords['char'] = 16
keywords['return'] = 17
keywords['const'] = 18
keywords['float'] = 19
keywords['short'] = 20
keywords['continue'] = 21
keywords['for'] = 22
keywords['void'] = 23
keywords['sizeof'] = 24

# 符号
keywords['#'] = 0
keywords['+'] = 27
keywords['-'] = 28
keywords['*'] = 29
keywords['/'] = 30
keywords['>'] = 36
keywords[':'] = 31
keywords['<'] = 33
"""
下面符号实验中未定义的额外标识符
"""
keywords[','] = 50
"""
下面符号由于是双字节，需要判断
"""
########################################
keywords['<>'] = 34
keywords['<='] = 35
keywords[':='] = 32
keywords['>='] = 37
########################################
keywords['='] = 38
keywords[';'] = 41
keywords['('] = 42
keywords[')'] = 43
keywords['['] = 44
keywords[']'] = 45
keywords['{'] = 46
keywords['}'] = 47


def preprocess():
    C_Rule_1 = "//.*"                   # 匹配C++中的'//'注释
    C_Rule_2 = "/\*.*\*/"               # 匹配C++中的'/**/'注释
    """
    ps1 = re.compile(C_Rule_1)
    ps2 = re.compile(C_Rule_2)
    """
    # line = ''
    newline = ''
    with open('raw.txt', 'r+') as f1:
        for line in f1:
            newline += line
    # print(newline)
    newline = ' '.join(re.sub(C_Rule_1, "", newline).split())
    # print(newline)
    finaltxt = ' '.join(re.sub(C_Rule_2, "", newline).split())
    with open("reproccessed.txt", 'w+') as f2:
        test = f2.write(finaltxt)
    return


def save(string):
    string = string.strip()
    if string in keywords.keys():
        print("<", keywords[string], ",", string, ">")
    else:
        try:
            # print(string)
            num = float(string)               # NUM
            # print(num)
            print("<", '26(NUM)', ",", string, ">")
        except ValueError:
            save_var(string)


def save_var(string):
    if len(string.strip()) < 1:
        pass
    else:
        if is_signal(string) == 1:      # ID
            print("<", '25(ID)', ",", string, ">")
        else:
            print("<", 'error501', ",", string, ">")       # 错误。


# def save_const(string):
#     print("<", string, ",", keywords[string], ">")


def is_signal(s):
    s = s.strip()
    if s[0] in string.ascii_letters+' ':
        for i in s:
            if i in string.ascii_letters or i in string.digits+' ':
                pass
            else:
                return 0
        return 1
    elif s[0] in string.digits:
        for q in s:
            if q in string.digits:
                pass
            else:
                return 0
        return 2


def analysis():
    with open("reproccessed.txt", 'r+') as f3:
        charlist = f3.read()
        key = ""
        sign = 0
    normal_signal = ['+', '-', '*', '/', ';', '(', ')', '#', '[', ']', '{', '}', ',']
    for i in charlist:
        if i == ' ':
            if len(key.strip()) < 0:
                sign = 0
                pass
            else:
                key += i
                save(key)
                key = ""
                sign = 0
        elif i in normal_signal:
            save(key)
            key = ""
            save(i)
            sign = 0
        elif i == ':' or i == '<':
            save(key)
            key = i
            sign = 1
        elif i == '=':
            if sign == 1 or key == '>':
                key += i
                save(key)
                key = ""
                sign = 0
            elif sign == 0:
                save(key)
                save(i)
                key = ""
        elif i == '>':
            if sign == 1 and key == '<':
                key += i
                save(key)
                key = ""
                sign = 0
            else:
                save(key)
                key = ""
                save(i)
        else:
            if key == '<' or key == '>':
                save(key)
                key = ""
            key += i
            # print(key)
    # for i in signlist.keys():
    #     print("<", signlist[i], ",", i, ">")


if __name__ == "__main__":
    preprocess()
    analysis()
