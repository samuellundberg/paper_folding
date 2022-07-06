import numpy as np


def get_creases(f, c):
    if type(f) != int or type(c) != int:
        print("input must be integers, exiting")
        return "error"
    if f < 2 or f > 5000:
        print("incorrect input for folds, exiting")
        return "error"
    if c < 1 or c > 2 ** f - 3:
        print("This crease will not exist given input folds, exiting")
        return "error"

    count = 2
    creases = np.array([-1, -1, 1])
    middle = np.array([-1])
    while count <= f:
        creases = np.concatenate((creases, middle, np.flip(-creases)))
        count += 1

    ans = array2string(creases[c - 1:c + 2])

    return ans


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


res = get_creases(25, 12)
print(res)
