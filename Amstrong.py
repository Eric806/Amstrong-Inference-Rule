class Indexs:
    def __init__(self, name):
        self.name = name
        self.belongs = []

    def addBelongs(self, belongs):
        self.belongs.append(belongs)

    def checkBelongs(self, statement):
        check = False
        be = ''
        for b in self.belongs:
            check = True
            for bs in b:
                if bs not in statement:
                    check = False
                    break
            if check:
                be = b
                break
        return check, f'{be}->{self.name}'

indexs_amount = int(input("輸入屬性數(自動生成A-Z的字母代表屬性名稱)："))
proveDict = {}  #證明字典

def strp(proveDict):    #把證明字典轉字串
    s = ''
    for k, v in proveDict.items():
        if v:
            s += k
    return s

def addp(statement):    #加入證明
    for s in statement:
        proveDict[s] = True

#屬性字典
indexDict = {}
for i in range(indexs_amount):
    indexDict[chr(65 + i)] = Indexs(chr(65 + i))
    proveDict[chr(65 + i)] = False
    
rules_amount = int(input("輸入規則數："))
print("輸入功能相依(英文全大寫，以'->'分隔，例：A->B)")

#加入分解規則
for i in range(rules_amount):
    l, r = input().split("->")
    if len(r) == 1:
        indexDict[r].addBelongs(l)
    else:
        for s in r:
            indexDict[s].addBelongs(l)
            print(f'新增規則 {l}->{s} (by 分解規則)')

#反身規則
pl, pr = input("輸入欲證明的功能相依(例：A->B)：").split("->")
steps = 1
addp(pl)
print(f'{steps}.{pl}->{strp(proveDict)} (by 反身規則)')
steps += 1

#聯集規則
for k, v in proveDict.items():
    if not v:
        check, be = indexDict[k].checkBelongs(pl)
        if check:
            addp(k)
            print(f'{steps}.{pl}->{strp(proveDict)} (by 聯集規則 from {be})')
            steps += 1

#遞移規則
change = True
while change:
    change = False
    p = strp(proveDict)
    for k, v in proveDict.items():
        if not v:
            check, be = indexDict[k].checkBelongs(p)
            if check:
                addp(k)
                print(f'{steps}.{pl}->{strp(proveDict)} (by 遞移規則 from {be})')
                steps += 1
                change = True
    
#測試是否包含
p = strp(proveDict)
check = True
for s in pr:
    if s not in p:
        check = False
        print(f'結論：無法證明{pl}->{pr}')
        break
    
if check:
    print(f'結論：可證明{pl}->{pr} (by 分解規則 from {pl}->{p})')

input()
