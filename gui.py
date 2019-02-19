from tkinter import *
import time
import json
import sys


sys.setrecursionlimit(1000000)

tom = Tk()
tom.geometry("272x272+0+-20")

mi = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
mj = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

f = open('m6.json', 'r')
mt = json.load(f)


def mf(i):
    if i < len(mt):
        for x in range(4):
            for y in range(4):
                mi[x][y] = PhotoImage(file='gif\\' + str(mt[i][x][y]) + '.gif')
                mj[x][y].configure(image=mi[x][y])

        tom.update()
        tom.after(0, mf(i+1))


for xi in range(4):
    for yi in range(4):
        mi[xi][yi] = PhotoImage(file='gif\\' + str(mt[0][xi][yi]) + '.gif')
        mj[xi][yi] = Label(tom, image=mi[xi][yi])
        mj[xi][yi].grid(row=xi, column=yi)
tom.update()
tom.after(0, mf, 0)
tom.mainloop()