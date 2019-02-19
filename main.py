import datetime
import ai
import json
import random as r

'''

    游戏实现、算法、结果可视化代码全部由本人手写完成
    本人非计科学生，代码能力较差

                programmer 赵胤
    
    main.py     代码主程序
    game.py     2048游戏实现逻辑
    test.py     状态评分函数
    ai.py       算法主程序
    gui.py      可视化（使用json文件中介）
    gif/xx.gif  图像文件（用于可视化）
    2048.pptx	课堂展示ppt

'''

start_time = datetime.datetime.now()

lse = []
l2 = []
a = 0
times = 100       # 运行的次数
for i in range(times):
    me, se, ae, meo = ai.ai()
    lse.append(se)
    l2.append(se**2)
    a += ae
with open('m.json', 'w', encoding="utf8") as fi:
    json.dump(meo, fi, ensure_ascii=False, indent=4)
print(lse, sum(lse)/len(lse), max(lse), a,)
e = sum(lse)/len(lse)
for i in lse:
    print(i, end='\t')
    if (lse.index(i)+1) % 10 == 0:
        print('')


c = sum(l2)/len(l2)
print(lse)
print(c, e, c-e*e)
end_time = datetime.datetime.now()
print((end_time - start_time).seconds, 's')