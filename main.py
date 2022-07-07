import numpy as np
import random as rd


def check_input(f, c):
    if type(f) != int or type(c) != int:
        print("input must be integers, exiting")
        return 1
    if f < 2 or f > 5000:
        print("incorrect input for folds, exiting")
        return 1
    if c < 1 or c > 2 ** f - 3:
        print("This crease will not exist given input folds, exiting")
        return 1
    return 0


def array2string(v):
    l = ''
    for e in v:
        if e == -1:
            l += "D"
        elif e == 1:
            l += "U"
        else:
            return "error"
    return l


def get_min_folds(c):
    f_new = 1
    while 2 ** f_new - 1 < c:
        f_new += 1
    return f_new


def back_track(f, c):
    cn = 2 ** f - 1
    mid = 2 ** (f - 1)
    count = 0
    raw_count = 0

    while f > 25:
        if c > cn or c < 1:
            return "error"

        if c == mid:
            return 2, 2, 1
        elif c > mid:
            c = cn - c + 1
            count += 1

        f -= 1
        cn = 2 ** f - 1
        mid = 2 ** (f - 1)
        raw_count += 1

    sign = (-1) ** count
    return f, c, sign


def get_crease(f, c, sign=0):
    count = 2
    creases = np.array([-1, -1, 1])
    middle = np.array([-1])
    while count <= f:
        creases = np.concatenate((creases, middle, np.flip(-creases)))
        count += 1

    if sign == 0:
        ans = array2string(creases[c - 1:c + 2])
    else:
        ans = array2string(sign * [creases[c - 1]])

    return ans


def main(f, c):
    if check_input(f, c) != 0:
        return "error"

    f_nec = get_min_folds(c)
    return get_crease(f_nec, c)


def main2(f, c):
    if check_input(f, c) != 0:
        return "error"

    f = get_min_folds(c)
    ans = ''
    for i in range(3):
        ci = c + i
        f_small, c_small, sign = back_track(f, ci)
        r = get_crease(f_small, c_small, sign)
        ans = ans + r
    return ans


rnum = rd.randint(0, 2**21)
print(rnum)
print("start main")
print(main(30, rnum))
print("finished main")
print("start main2")
print(main2(5000, rnum))
print("finished main2")
