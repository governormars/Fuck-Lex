#!/usr/bin/python3
# -*-coding=utf-8
import re

"""
（1）E->TG
（2）G->+TG|—TG
（3）G->ε
（4）T->FS
（5）S->*FS|/FS
（6）S->ε
（7）F->(E)
（8）F->i
"""

# G = {'E': ['TG'], 'G': ['+TG', '-TG', 'ε'], 'T': ['FS'], 'S': ['*FS', '/FS', 'ε'], 'F': ['(E)', 'i']}      # 产生式
G = ['E->TG', 'G->+TG', 'G->-TG', 'G->ε', 'T->FS', 'S->*FS', 'S->/FS', 'S->ε', 'F->(E)', 'F->i']        # 产生式
Vt = ['i', '+', '-', '*', '/', '(', ')', '#']             # 终结符号
Vn = ['E', 'T', 'G', 'F', 'S']               # 非终结符号
Va = Vt + Vn        # 字符集

First = {}          # first
firstAll = []
Follow = {}         # follow
PreStack = []       # 分析栈
Flag_First = {'E': 0, 'T': 0, 'G': 0, 'F': 0, 'S': 0, 'i': 0, '+': 0, '-': 0, '*': 0, '/': 0, '(': 0, ')': 0, '#': 0}
Flag_Follow = {'E': 0, 'T': 0, 'G': 0, 'F': 0, 'S': 0}
M = {}              # 预测分析表
# 初始化
for i in range(len(Vn)):
    for q in range(len(Vt)):
        M[Vn[i], Vt[q]] = ' '


def filterG(s):
    find_lst = re.findall(r"(.*?)->(.*)", s)
    return(find_lst)


# def initGrammer():
#     with open('Grammer.txt', 'r+') as f:
#         for line in f:
#             if '->' not in line:
#                 print('wrong grammer!')
#                 exit()
#             eles

def getFirst(a):
    if a in Vt:
        First[a] = [a]
        Flag_First[a] = 1
    if a in Vn and Flag_First[a] == 0:
        First[a] = []
        for i in range(len(G)):
            notTChar = filterG(G[i])[0][0]           # 产生式左部非终结符
            followChar = filterG(G[i])[0][1]         # 产生式右部字符串
            # 判断终结符
            if a == notTChar:
                for n in range(len(followChar)):
                    # if 产生式右部第一个字符为终结符或空 then 把a或e加进FIRST(a)
                    if followChar[0] in Vt or followChar[0] == 'ε':
                        First[a].append(followChar[0])
                        break
                    else:
                        # if 产生式右部第n个字符没有求first集
                        if Flag_First[followChar[n]] == 0:
                            getFirst(followChar[0])
                            # 求并集
                            First[a] = list(set(First[a]).union(set(First[followChar[n]])))
                        if 'ε' not in First[followChar[n]]:
                            break
                        # if 空串不包含在最后一个字符的first集合中，那就剔除
                        elif 'ε' in First[followChar[n]] and n != (len(followChar) - 1):
                            # 去除空串
                            First[a] = list(set(First[a]) ^ set('ε'))
                            continue
        Flag_First[a] = 1

Vs = filterG(G[0])[0][0]        # 文法的开始字符
for q in Vn:
    Follow[q] = []
Follow[Vs] = ['#']

def getFollow(a):
    # 遍历产生式
    for i in range(len(G)):
        notTChar = filterG(G[i])[0][0]  # 产生式左部非终结符
        followChar = filterG(G[i])[0][1]  # 产生式右部字符串
        if a in followChar:
            # b -> ....a
            if a == followChar[-1]:
                if Flag_Follow[notTChar] == 1:
                    Follow[a] = list(set(Follow[a]).union(set(Follow[notTChar])))
                elif a != notTChar:
                    getFollow(notTChar)
            else:
                pos = followChar.index(a)
                for n in range(pos+1, len(followChar)):
                    # b -> ...a终结符...
                    if followChar[n] in Vt:
                        if followChar[n] not in Follow[a]:
                            Follow[a].append(followChar[n])
                        break
                    # b -> ...acdef...
                    if 'ε' not in First[followChar[n]]:
                        Follow[a] = list(set(Follow[a]).union(set(First[followChar[n]])))
                        break
                    if 'ε' in First[followChar[n]]:
                        Follow[a] = list(set(Follow[a]).union(set(First[followChar[n]])) ^ set('ε'))
                        if n == (len(followChar)-1):
                            if Flag_Follow[notTChar] == 1:
                                Follow[a] = list(set(Follow[a]).union(set(Follow[notTChar])))
                                break
                            elif a != notTChar:
                                getFollow(notTChar)
    Flag_Follow[a] = 1

for n in Va:
    getFirst(n)

for q in Vn:
    getFollow(q)

def getPredictChart():
    for i in range(len(G)):
        notTChar = filterG(G[i])[0][0]  # 产生式左部非终结符
        followChar = filterG(G[i])[0][1]  # 产生式右部字符串
        firstAll = []   # 初始化产生式右部first集合
        for n in followChar:
            if n == 'ε':
                firstAll.append('ε')
                break
            elif 'ε' in First[n]:
                firstAll = list(set(firstAll).union(set(First[n])) ^ set('ε'))
            elif 'ε' not in First[n]:
                firstAll = list(set(firstAll).union(set(First[n])))
                break

        if 'ε' == followChar:
            for b in Follow[notTChar]:
                M[(notTChar, b)] = G[i]
            continue
        for t in Vt:
            if t in firstAll:
                M[(notTChar, t)] = G[i]
        if 'ε' in firstAll:
            for b in Follow[notTChar]:
                M[(notTChar, b)] = G[i]
    """
    打印模块
    """
    print("PREDICT CHART:")
    print('          ', end="")
    for z in Vt:
        print('{:<10}'.format(z), end="")
        # print('%-10s' % z, end="")
    print('\n')
    for x in Vn:
        print('%-10s' % x, end="")
        for c in Vt:
            print('%-10s' % (M[(x, c)]), end="")
        print('\n')

getPredictChart()

def predict():
    lan = input("请输入文法：")
    PreStack = []
    # '#', 开始符入栈
    PreStack.append('#')
    PreStack.append(Vs)
    count = 0           # 输入串index
    step = 0            # 操作步骤自增
    print('step            stack            string            used-rule')
    while count < len(lan):
        step += 1
        if step == 1:
            print('%-16d%-17s%-18s' % (step, ''.join(PreStack), lan))
        x = PreStack.pop()
        if x in Vn:
            str = filterG(M[(x, lan[count])])[0][1]
            print('%-16d%-17s%-18s%s' % (step, ''.join(PreStack), lan[count:], M[(x, lan[count])]))
            for p in str[::-1]:
                # print(filterG(M[(x, a)])[0][1])
                if p == 'ε':
                    continue
                else:
                    PreStack.append(p)
        if x in Vt:
            print('%-16d%-17s%-18s' % (step, ''.join(PreStack), lan[count:]))
            if x == '#' and lan[count] == '#':
                print('success!!!')
                break
            elif x == lan[count]:
                count += 1
            else:
                print('wrong!')
                break

predict()








