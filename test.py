import re
G = ['E->TG', 'G->+TG', 'G->-TG', 'G->ε', 'T->FS', 'S->*FS', 'S->/FS', 'S->ε', 'F->(E)', 'F->i23']
def filterG(s):
    find_lst = re.findall(r"(.*?)->(.*)", s)
    return(find_lst)
print (filterG(G[6]), G[9])
First = {}
First['a'] = ['saasdsadasdsad']
First['a'].append('asdasd')
if 'i' == filterG(G[9])[0][1][0]:

    print('fuck')
print(G[2][0][0])
First['1'] = []
First['1'].append('213213')
print(First)
a = [1,2,3]
b= '$'
ret = list(set(a) ^ set(b))
print(ret)
s = '123456'
d = [1,2,3,4,5,6,7]
for n in range(len(d)):
    print(n, d[n], len(d))
print('12345657850'[-2])
q='123456'
if '5' == q[-2]:
    print(12222222222222222222)
for n in range(len('123456')):
    print(n)
fuck = 'abcdef'
print(fuck[1:])