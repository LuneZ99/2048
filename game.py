import random as r
import copy


def up(mu, si):
    # print('↑')
    for ui in (3, 2, 1, 0):
        for i in range(3):
            for u2 in (2, 1, 0):
                if mu[u2][ui] == 0:
                    mu[u2][ui] = mu[u2+1][ui]
                    mu[u2+1][ui] = 0

        if mu[0][ui] == mu[1][ui]:
            mu[0][ui] *= 2
            mu[1][ui] = mu[2][ui]
            mu[2][ui] = mu[3][ui]
            mu[3][ui] = 0
            si += mu[0][ui]
        if mu[1][ui] == mu[2][ui]:
            mu[1][ui] *= 2
            mu[2][ui] = mu[3][ui]
            mu[3][ui] = 0
            si += mu[1][ui]
        if mu[2][ui] == mu[3][ui]:
            mu[2][ui] *= 2
            mu[3][ui] = 0
            si += mu[2][ui]
    return si


def down(md, si):
    # print('↓')
    for ui in (3, 2, 1, 0):
        for i in range(3):
            for u2 in (1, 2, 3):
                if md[u2][ui] == 0:
                    md[u2][ui] = md[u2-1][ui]
                    md[u2-1][ui] = 0
        if md[3][ui] == md[2][ui]:
            md[3][ui] *= 2
            md[2][ui] = md[1][ui]
            md[1][ui] = md[0][ui]
            md[0][ui] = 0
            si += md[3][ui]
        if md[2][ui] == md[1][ui]:
            md[2][ui] *= 2
            md[1][ui] = md[0][ui]
            md[0][ui] = 0
            si += md[2][ui]
        if md[1][ui] == md[0][ui]:
            md[1][ui] *= 2
            md[0][ui] = 0
            si += md[1][ui]
    return si


def left(ml, si):
    # print('←')
    for ui in (3, 2, 1, 0):
        for i in range(3):
            for u2 in (2, 1, 0):
                if ml[ui][u2] == 0:
                    ml[ui][u2] = ml[ui][u2+1]
                    ml[ui][u2+1] = 0

        if ml[ui][0] == ml[ui][1]:
            ml[ui][0] *= 2
            ml[ui][1] = ml[ui][2]
            ml[ui][2] = ml[ui][3]
            ml[ui][3] = 0
            si += ml[ui][0]
        if ml[ui][1] == ml[ui][2]:
            ml[ui][1] *= 2
            ml[ui][2] = ml[ui][3]
            ml[ui][3] = 0
            si += ml[ui][1]
        if ml[ui][2] == ml[ui][3]:
            ml[ui][2] *= 2
            ml[ui][3] = 0
            si += ml[ui][2]
    return si


def right(mr, si):
    # print('→')
    for ui in (0, 1, 2, 3):
        for i in range(3):
            for u2 in (3, 2, 1):
                if mr[ui][u2] == 0:
                    mr[ui][u2] = mr[ui][u2-1]
                    mr[ui][u2-1] = 0

        if mr[ui][3] == mr[ui][2]:
            mr[ui][3] *= 2
            mr[ui][2] = mr[ui][1]
            mr[ui][1] = mr[ui][0]
            mr[ui][0] = 0
            si += mr[ui][3]
        if mr[ui][2] == mr[ui][1]:
            mr[ui][2] *= 2
            mr[ui][1] = mr[ui][0]
            mr[ui][0] = 0
            si += mr[ui][2]
        if mr[ui][1] == mr[ui][0]:
            mr[ui][1] *= 2
            mr[ui][0] = 0
            si += mr[ui][1]
    return si


def au(mu):
    temp = 0
    for pi in (0, 1, 2, 3):
        if mu[0][pi] == 0 and (mu[1][pi] != 0 or mu[2][pi] != 0 or mu[3][pi] != 0):
            temp = 1
            break
        if mu[1][pi] == 0 and (mu[2][pi] != 0 or mu[3][pi] != 0):
            temp = 1
            break
        if mu[2][pi] == 0 and mu[3][pi] != 0:
            temp = 1
            break
        if (mu[0][pi] == mu[1][pi] and mu[0][pi] != 0) \
                or (mu[1][pi] == mu[2][pi] and mu[1][pi] != 0) \
                or (mu[2][pi] == mu[3][pi] and mu[2][pi] != 0):
            temp = 1
            break
    return temp


def ad(mu):
    temp = 0
    for pi in (0, 1, 2, 3):
        if mu[3][pi] == 0 and (mu[2][pi] != 0 or mu[1][pi] != 0 or mu[0][pi] != 0):
            temp = 1
            break
        if mu[2][pi] == 0 and (mu[1][pi] != 0 or mu[0][pi] != 0):
            temp = 1
            break
        if mu[1][pi] == 0 and mu[0][pi] != 0:
            temp = 1
            break
        if (mu[0][pi] == mu[1][pi] and mu[0][pi] != 0) \
                or (mu[1][pi] == mu[2][pi] and mu[1][pi] != 0) \
                or (mu[2][pi] == mu[3][pi] and mu[2][pi] != 0):
            temp = 1
            break
    return temp


def al(mu):
    temp = 0
    for pi in (0, 1, 2, 3):
        if mu[pi][0] == 0 and (mu[pi][1] != 0 or mu[pi][2] != 0 or mu[pi][3] != 0):
            temp = 1
            break
        if mu[pi][1] == 0 and (mu[pi][2] != 0 or mu[pi][3] != 0):
            temp = 1
            break
        if mu[pi][2] == 0 and mu[pi][3] != 0:
            temp = 1
            break
        if (mu[pi][0] == mu[pi][1] and mu[pi][0] != 0)\
                or (mu[pi][1] == mu[pi][2] and mu[pi][1] != 0)\
                or (mu[pi][2] == mu[pi][3] and mu[pi][2] != 0):
            temp = 1
            break
    return temp


def ar(mu):
    temp = 0
    for pi in (0, 1, 2, 3):
        if mu[pi][3] == 0 and (mu[pi][2] != 0 or mu[pi][1] != 0 or mu[pi][0] != 0):
            temp = 1
            break
        if mu[pi][2] == 0 and (mu[pi][1] != 0 or mu[pi][0] != 0):
            temp = 1
            break
        if mu[pi][1] == 0 and mu[pi][0] != 0:
            temp = 1
            break
        if (mu[pi][0] == mu[pi][1] and mu[pi][0] != 0)\
                or (mu[pi][1] == mu[pi][2] and mu[pi][1] != 0)\
                or (mu[pi][2] == mu[pi][3] and mu[pi][2] != 0):
            temp = 1
            break
    return temp


def allow(mt, t):
    temp = 0
    if t == 1 and au(mt):
        temp = 1
    if t == 2 and ad(mt):
        temp = 1
    if t == 3 and al(mt):
        temp = 1
    if t == 4 and ar(mt):
        temp = 1
    return temp


def move(ma, t, si=0):

    mt = copy.deepcopy(ma)

    if t == 1:
        si = up(mt, si)
    if t == 2:
        si = down(mt, si)
    if t == 3:
        si = left(mt, si)
    if t == 4:
        si = right(mt, si)

    return mt, si


def gen(mt, flag):
    if flag:  # 若仍未死亡
        while True:  # 寻找一个空位生成2或4
            xt = r.randint(0, 3)
            yt = r.randint(0, 3)
            it = r.randint(1, 10)
            if mt[xt][yt] == 0:
                if 1 <= it <= 9:
                    mt[xt][yt] = 2
                else:
                    mt[xt][yt] = 4
                # print('G ('+str(xt+1)+', '+str(yt+1)+', '+str(2 * it)+')')
                return mt, xt, yt
    else:  # 若死亡
        # print('D')
        return mt, -1, -1


def gen_xy2(mt, xy):
    mt0 = copy.deepcopy(mt)
    mt0[xy[0]][xy[1]] = 2
    # print('G'+str(xy[0]+1)+str(xy[1]+1))
    return mt0


def gen_xy4(mt, xy):
    mt0 = copy.deepcopy(mt)
    mt0[xy[0]][xy[1]] = 4
    # print('G'+str(xy[0]+1)+str(xy[1]+1))
    return mt0


def main():                         # 随机移动的结果
    m_start = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    m = m_start
    step = 0

    while True:  # 第一次生成
        xt = r.randint(0, 3)
        yt = r.randint(0, 3)
        it = r.randint(1, 2)
        if m[xt][yt] == 0:
            m[xt][yt] = 2 * it
            break

    while True:

        flag = 0
        while True:
            if au(m)+ad(m)+al(m)+ar(m) == 0:    # 判断死亡
                print('You Dead!')
                s = 0
                for i in m:
                    for j in i:
                        s += j
                print('Your Score is', s)
                return s    # 输出分数

            flow = r.randint(1, 4)  # 上，下，左，右
            if flow == 1 and au(m):
                up(m)
                flag = 1
            if flow == 2 and ad(m):
                down(m)
                flag = 1
            if flow == 3 and al(m):
                left(m)
                flag = 1
            if flow == 4 and ar(m):
                right(m)
                flag = 1
            if flag:
                break

            # 此处需要对m的结果进行评价

        if flag:    # 若仍未死亡
            while True:     # 寻找一个空位生成2或4
                xt = r.randint(0, 3)
                yt = r.randint(0, 3)
                it = r.randint(1, 2)
                if m[xt][yt] == 0:
                    m[xt][yt] = 2 * it
                    break
        else:   # 若死亡
            break

        print('step' + str(step) + ':')     # 生成后的图样
        for i in m:
            for j in i:
                print(str(j) + '\t', end='', sep='')
            print('')

        step += 1   # 步数增长


'''

测试代码

m = [
    [2, 2, 4, 4],
    [2, 2, 4, 4],
    [2, 2, 4, 4],
    [2, 0, 0, 2]
]

s = left(m, 0)

for lin in m:
    print(lin)
print(s)


ls = []
ls.append(move(m, 3)[0])
print(ls)
'''