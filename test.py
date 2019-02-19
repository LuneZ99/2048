import random
import math
import game
'''
    sample of ma:
    ma = [
        [2, 4, 8, 2],
        [0, 0, 2, 4],
        [4, 0, 0, 0],
        [4, 4, 2, 2],
    ]
    '''


def test(ma, q=(2.72, 1, 72, 1, 10)):    # 矩阵，权重

    if game.allow(ma, 1) == 0 and game.allow(ma, 2) == 0 and game.allow(ma, 3) == 0 and game.allow(ma, 4) == 0:
        return float('-inf')

    a = 0                       # 评分项 a = 最大值 - 最大值位置惩罚
    al = []
    for a1 in ma:
        al.extend(a1)
    if al.index(max(al)) == 0 or al.index(max(al)) == 3 or al.index(max(al)) == 12 or al.index(max(al)) == 15:
        a += 27 * math.log(max(al), 2)

    if 0 <= al.index(max(al)) <= 4 or 11 <= al.index(max(al)) <= 15 or al.index(max(al)) == 7 or al.index(max(al)) == 8:
        a += 1
    al.sort(reverse=True)
    a += math.log(al[0]+1, 2) + math.log(al[1]+1, 2) + math.log(al[2]+1, 2) + math.log(al[3]+1, 2) - 1

    b = 0                           # 评分项 b = 单调性
    bt = 0
    for b1 in ma:
        for b2 in (0, 1, 2):
            if b1[b2] == b1[b2+1] and b1[b2] != 0:
                b += 1
            elif b1[b2] > b1[b2+1]:
                b += 1
            elif b1[b2] < b1[b2+1]:
                b -= 1
        bt += abs(b)
        b = 0
    for b4 in (0, 1, 2, 3):
        for b3 in (0, 1, 2):
            if ma[b3][b4] == ma[b3+1][b4] and ma[b3][b4] != 0:
                b += 1
            elif ma[b3][b4] > ma[b3+1][b4]:
                b += 1
            elif ma[b3][b4] < ma[b3+1][b4]:
                b -= 1
        bt += abs(b)
        b = 0
    b = bt

    c = 0                           # 评分项 c = 空格数 ∈ [0, 16]
    for c1 in ma:
        for c2 in c1:
            if c2 == 0:
                c += 1
    ce = c
    c = math.log((c+1)/32)

    d = 0                           # 评分项 d = 空格汇聚程度 ∈ [0, 24]
    for d1 in (0, 1, 2):
        for d2 in (0, 1, 2, 3):
            if ma[d1][d2] == 0:
                d += not ma[d1+1][d2]
    for d1 in (0, 1, 2, 3):
        for d2 in (0, 1, 2):
            if ma[d1][d2] == 0:
                d += not ma[d1][d2+1]

    e = 0                           # 评分项 e = 均匀度 ∈ (-inf, 0]
    for e1 in ma:
        for e2 in (0, 1, 2):
            if e1[e2] != e1[e2+1]:
                e += math.log(abs(e1[e2] - e1[e2+1]), 2)
    for e3 in (0, 1, 2):
        for e4 in (0, 1, 2, 3):
            if ma[e3][e4] != ma[e3+1][e4]:
                e += math.log(abs(ma[e3][e4] - ma[e3+1][e4]), 2)
    e = -e * (16 - c)

    s = q[0] * a + q[1] * b + q[2] * c + q[3] * d + q[4] * e    # 总分

    return s
