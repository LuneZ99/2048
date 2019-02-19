import random as r
import game as g
import test as t
import datetime
import copy as c
import pprin
import json
import math



def score(mt, qt):

    si = 0                   # 此项无用
    ls = [[], [], [], []]    # 上 下 左 右 移动一步，所有生成情况的评分表   f ∈ (-inf, inf)
    dl2 = [[], [], [], []]   # 评分表对应位置的生成坐标与值    (x, y, 2or4)

    for d1 in (1, 2, 3, 4):

        if g.allow(mt, d1) != 1:
            ls[d1 - 1] = [-float('inf')]
            dl2[d1 - 1] = []
            continue

        mp, si = g.move(mt, d1, si)

        dl1 = []
        for x in (0, 1, 2, 3):
            for y in (0, 1, 2, 3):
                if mp[x][y] == 0:
                    dl1.append((x, y))

        for d2 in dl1:
            md = g.gen_xy2(mp, d2)
            ls[d1 - 1].append(t.test(md))
            dl2[d1 - 1].append((d2[0], d2[1], 2))

            md = g.gen_xy4(mp, d2)
            ls[d1 - 1].append(t.test(md, qt))
            dl2[d1 - 1].append((d2[0], d2[1], 4))
    '''
    for line in ls:
        print(line)
    for line in dl2:
        print(line)
    '''
    return ls, dl2


# 随机选择可行的方向
def choose_random(m0):
    while True:
        ran = r.randint(1, 4)
        if g.allow(m0, ran):
            return ran


# 假设生成在最佳位置，选择最佳方向（贪婪算法）
def choose_max_max(m0, q0):    # 选择可能出现最优生成的方向
    ls1, dl1 = score(m0, q0)  # 输入m，生成评分表及对应位置表
    lt = []
    for l1 in ls1:
        lt.append(max(l1))
    li1 = lt.index(max(lt))  # li1+1 == 最大情况移动方向
    li2 = ls1[li1].index(max(ls1[li1]))
    # print(ls[li1][li2])
    # print(li1+1, '('+str(dl2[li1][li2][0]+1)+', '+str(dl2[li1][li2][1]+1)+', '+str(dl2[li1][li2][2])+')')
    return li1+1


# 单层
def choose_min_max(m0, q0):
    dic = {}
    for d1 in (1, 2, 3, 4):
        if g.allow(m0, d1):
            dic[d1] = {'m': g.move(m0, d1)[0]}
            for d2 in range(4):
                for d3 in range(4):
                    if dic[d1]['m'][d2][d3] == 0:
                        dic[d1][str(d2) + str(d3) + '2'] = g.gen_xy2(dic[d1]['m'], (d2, d3))
                        dic[d1][str(d2) + str(d3) + '4'] = g.gen_xy4(dic[d1]['m'], (d2, d3))
            del(dic[d1]['m'])

    for c1 in dic:
        if c1 != {}:
            for c2 in dic[c1]:
                dic[c1][c2] = t.test(dic[c1][c2])

    for c1 in dic:
        if c1 != {}:
            dic[c1] = dic[c1][min(dic[c1], key=dic[c1].get)]
        else:
            dic[c1] = float('-inf')

    d = max(dic, key=dic.get)

    return d


# 模拟退火附加
def choose_ex(m0, q0):
    dic = {}
    for d1 in (1, 2, 3, 4):
        if g.allow(m0, d1):
            dic[d1] = {'m': g.move(m0, d1)[0]}
            for d2 in range(4):
                for d3 in range(4):
                    if dic[d1]['m'][d2][d3] == 0:
                        dic[d1][str(d2) + str(d3) + '2'] = g.gen_xy2(dic[d1]['m'], (d2, d3))
                        dic[d1][str(d2) + str(d3) + '4'] = g.gen_xy4(dic[d1]['m'], (d2, d3))
            del (dic[d1]['m'])

    for c1 in dic:
        if c1 != {}:
            for c2 in dic[c1]:
                dic[c1][c2] = t.test(dic[c1][c2])

    for c1 in dic:
        if c1 != {}:
            dic[c1] = dic[c1][min(dic[c1], key=dic[c1].get)]
        else:
            dic[c1] = float('-inf')

    k = 0
    for i in m0:
        for j in i:
            if j == 0:
                k += 1

    dm = max(dic, key=dic.get)
    for c1 in dic:
        if c1 != dm:
            p = r.random()
            if p < math.exp(((dic[c1]-dic[dm])/(k+1))):
                return c1
    return dm


# 对所有生成位置进行平均，选择最佳方向（无意义，放弃）
def choose_avg_max(m0, q0):
    ls1, dl1 = score(m0, q0)  # 输入m，生成评分表及对应位置表
    lt = []
    for l1 in ls1:
        lt.append(sum(l1)/len(l1))
    li1 = lt.index(max(lt))  # li1+1 == 最大情况移动方向
    li2 = ls1[li1].index(max(ls1[li1]))
    # print(ls[li1][li2])
    # print(li1+1, '('+str(dl2[li1][li2][0]+1)+', '+str(dl2[li1][li2][1]+1)+', '+str(dl2[li1][li2][2])+')')
    return li1+1


# 限制深度进行多层搜索，以可能性为期望选择最佳方向（使用list，效率过低，放弃）
def choose_max_depth(m0, q0, d0):
    dt = 0
    mt = c.deepcopy(m0)
    lst0 = []
    lst0.append(mt)
    lst1 = []
    mf = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    while True:
        dt += 1

        for jt in lst0:
            for it in (1, 2, 3, 4):
                if dt == 1:
                    lst1.append((g.move(jt, it)[0], it))
                else:
                    lst1.append((g.move(jt[0], it)[0], jt[1]))
        lst0 = []
        for m1 in lst1:
            for xt in range(3):
                for yt in range(3):
                    if m1[0][xt][yt] == 0:
                        lst0.append((g.gen_xy2(m1[0], (xt, yt)), m1[1]))
                        lst0.append((g.gen_xy4(m1[0], (xt, yt)), m1[1]))

        if dt == d0:
            break

    dr = []
    for mr in lst0:
        dr.append(t.test(mr[0], q0))
    s = dr.index(max(dr))
    return lst0[s][1]


# 限制深度进行多层搜索，以可能性为期望选择最佳方向（使用dict）
def choose_max_depth_dic(m0, q0, d0):

    mt = c.deepcopy(m0)
    dic = {
        'm': mt
    }
    for a1 in ('1', '2', '3', '4'):
        if g.allow(dic['m'], int(a1)):
            dic[a1] = {
                'm': g.move(dic['m'], int(a1), 0)[0]
                }
    # for a1 in dic:
    #     if a1 != 'm':
            for xt in range(4):
                for yt in range(4):
                    if dic[a1]['m'][xt][yt] == 0:
                        dic[a1][str(xt) + str(yt) + '2'] = {'m': g.gen_xy2(dic[a1]['m'], (xt, yt))}
                        dic[a1][str(xt) + str(yt) + '4'] = {'m': g.gen_xy4(dic[a1]['m'], (xt, yt))}

    for b1 in dic:
        if b1 != 'm':
            for b2 in dic[b1]:
                if b2 != 'm':
                    for b3 in ('1', '2', '3', '4'):
                        if g.allow(dic[b1][b2]['m'], int(b3)):
                            dic[b1][b2][b3] = {'m': g.move(dic[b1][b2]['m'], int(b3), 0)[0]}
                            for xt in range(4):
                                for yt in range(4):
                                    if dic[b1][b2][b3]['m'][xt][yt] == 0:
                                        dic[b1][b2][b3][str(xt) + str(yt) + '2'] = {
                                            'm': g.gen_xy2(dic[b1][b2][b3]['m'], (xt, yt))}
                                        dic[b1][b2][b3][str(xt) + str(yt) + '4'] = {
                                            'm': g.gen_xy4(dic[b1][b2][b3]['m'], (xt, yt))}

    alpha = float('+inf')
    beta = float('-inf')

    for c1 in dic:
        if c1 != 'm':
            for c2 in dic[c1]:
                if c2 != 'm':
                    for c3 in dic[c1][c2]:
                        if c3 != 'm':
                            for c4 in dic[c1][c2][c3]:
                                if c4 != 'm':
                                    for c5 in ('1', '2', '3', '4'):
                                        if g.allow(dic[c1][c2][c3][c4]['m'], int(c5)):
                                            dic[c1][c2][c3][c4][c5] = {
                                                'm': g.move(dic[c1][c2][c3][c4]['m'], int(c5), 0)[0]
                                                }

                                            for xt in range(4):
                                                for yt in range(4):
                                                    if dic[c1][c2][c3][c4][c5]['m'][xt][yt] == 0:
                                                        dic[c1][c2][c3][c4][c5][str(xt) + str(yt) + '2'] = {
                                                            'm': g.gen_xy2(dic[c1][c2][c3][c4][c5]['m'], (xt, yt))
                                                            }
                                                        dic[c1][c2][c3][c4][c5][str(xt) + str(yt) + '4'] = {
                                                            'm': g.gen_xy4(dic[c1][c2][c3][c4][c5]['m'], (xt, yt))
                                                            }
                                        '''
                                        for c6 in dic[c1][c2][c3][c4][c5]:
                                            if c6 != 'm':
                                                dic[c1][c2][c3][c4][c5][c6] = t.test(
                                                    dic[c1][c2][c3][c4][c5][c6]['m'])
                                                if dic[c1][c2][c3][c4][c5][c6] < beta:
                                                    beta = dic[c1][c2][c3][c4][c5][c6]
                                                    break
                                        '''
    # pp = pprint.PrettyPrinter(indent=4, width=100)
    # pp.pprint(dic)
    del(dic['m'])
    for c1 in dic:
        del(dic[c1]['m'])
        for c2 in dic[c1]:
            del(dic[c1][c2]['m'])
            for c3 in dic[c1][c2]:
                del(dic[c1][c2][c3]['m'])
                for c4 in dic[c1][c2][c3]:
                    del(dic[c1][c2][c3][c4]['m'])
                    for c5 in dic[c1][c2][c3][c4]:
                        del (dic[c1][c2][c3][c4][c5]['m'])

    # pp = pprint.PrettyPrinter(indent=4, width=100)
    # pp.pprint(dic)
    for c1 in dic:
        for c2 in dic[c1]:
            for c3 in dic[c1][c2]:
                for c4 in dic[c1][c2][c3]:
                    for c5 in dic[c1][c2][c3][c4]:
                        for c6 in dic[c1][c2][c3][c4][c5]:
                            dic[c1][c2][c3][c4][c5][c6] = t.test(dic[c1][c2][c3][c4][c5][c6]['m'])

                        if dic[c1][c2][c3][c4][c5] != {}:
                            dic[c1][c2][c3][c4][c5] = dic[c1][c2][c3][c4][c5][
                                min(dic[c1][c2][c3][c4][c5], key=dic[c1][c2][c3][c4][c5].get)]
                        else:
                            dic[c1][c2][c3][c4][c5] = float('-inf')

                    if dic[c1][c2][c3][c4] != {}:
                        dic[c1][c2][c3][c4] = dic[c1][c2][c3][c4][max(dic[c1][c2][c3][c4], key=dic[c1][c2][c3][c4].get)]
                    else:
                        dic[c1][c2][c3][c4] = float('+inf')

                if dic[c1][c2][c3] != {}:
                    dic[c1][c2][c3] = dic[c1][c2][c3][min(dic[c1][c2][c3], key=dic[c1][c2][c3].get)]
                else:
                    dic[c1][c2][c3] = float('-inf')
            if dic[c1][c2] != {}:
                dic[c1][c2] = dic[c1][c2][max(dic[c1][c2], key=dic[c1][c2].get)]
            else:
                dic[c1][c2] = float('+inf')
        if dic[c1] != {}:
            dic[c1] = dic[c1][min(dic[c1], key=dic[c1].get)]
        else:
            dic[c1] = float('-inf')
    d = max(dic, key=dic.get)
    return int(d)


# 优先选择右/下，在无法右或下时选择左/上中较好的选择（贪婪算法）
def right_down_first(m0, q0):
    if g.ad(m0) and g.ar(m0):
        ls1, dl1 = score(m0, q0)  # 输入m，生成评分表及对应位置表
        lt = [max(ls1[0]), max(ls1[2])]
        li1 = lt.index(max(lt))  # li1+1 == 最大情况移动方向
        li2 = ls1[li1].index(max(ls1[li1]))
        # print(ls[li1][li2])
        # print(li1+1, '('+str(dl2[li1][li2][0]+1)+', '+str(dl2[li1][li2][1]+1)+', '+str(dl2[li1][li2][2])+')')
        return 2*li1 + 2
    if g.ad(m0):
        return 2
    if g.ar(m0):
        return 4
    return choose_max_max(m0, q0)


# 主代码
def ai():
    m_start = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

    m = m_start
    a_direction = (1, 2, 3, 4)
    q = [2.72, 1, 72, 1, 10]             # 最大值，单调性，空格数，汇聚度，均匀度
    s0 = 0
    mto = []

    # q = [1, 1, 1, 1, 1]  avg = 1400
    # q = [2.72, 1, 72, 1, 5.44]  avg16_max = 2100

    step = 0
    depth = 3
    fun = 'choose_avg_max()'
    # flag                          # 死亡判断 1 == 存活， 0 == 死亡

    for u1 in range(2):             # 生成初始面板
        while True:
            xt = r.randint(0, 3)
            yt = r.randint(0, 3)
            it = r.randint(1, 2)
            if m[xt][yt] == 0:
                m[xt][yt] = 2 * it
                break

    # print('')
    # for line in m:                     # 打印初始面板
    #     print(line)
    # print('')

    while True:

        flag = 0  # 判断死亡
        for d1 in a_direction:
            if g.allow(m, d1):
                flag = 1
        if not flag:
            ap = 0
            for line in m:
                if 2048 in line or 4096 in line or 8192 in line:
                    ap = 1
            # print('')
            # for line in m:  # 打印结束面板
            #     print(line)
            # print('')
            print('Dead! Score =', s0)
            return m, s0, ap, mto

        mp = []
        for line in m:
            mp.extend(line)
        mp.sort(reverse=True)

        # if mp[14] == 0:
        #     d = choose_min_max(m, q)
        # else:
        #     d = choose_max_depth_dic(m, q, 3)
        if mp[15] == 0 or mp[14] != 0:

            d = choose_min_max(m, q)
            # d = choose_ex(m, q)
        m, s0 = g.move(m, d, s0)
        # print(('↑', '↓', '←', '→')[d-1])
        m, x, y = g.gen(m, flag)
        # dls0.append(d)
        # print('')
        # for line in m:
        #     print(line)
        mto.append(m)


# '''

# main

'''
start_time = datetime.datetime.now()

lse = []
dls0 = []
dls1 = []
a = 0
times = 1
for i in range(times):
    me, se, ae, meo = ai()
    lse.append(se)
    dls1.append(dls0)
    dls0 = []
    a += ae
with open('m.json', 'w', encoding="utf8") as fi:
    json.dump(meo, fi, ensure_ascii=False, indent=4)
print(lse, sum(lse)/len(lse), max(lse), a)
'''
'''
print(dls1, lse)
dlj = json.dumps(dls1)
lsj = json.dumps(lse, sort_keys=True, indent=4, separators=(',', ': '))
with open('a.json', 'w') as f:
    f.write(dlj)
f.close()
with open('b.json', 'w') as f1:
    f1.write(lsj)
f1.close()

end_time = datetime.datetime.now()
print((end_time - start_time).seconds, 's')

'''
