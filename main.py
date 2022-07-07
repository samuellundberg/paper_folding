import numpy as np
from numpy import random
import random as rd
import time


def check_input(f, c):
    # Check if input values are integers and inside criteria limits
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
    # transformes list of -1 and 1 to U/D string
    # ex. [-1,-1,1] -> "DDU"
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
    # Find the smallest f that contains c
    # Important for old solver but basically redundant when using back_track()
    f_new = 1
    while 2 ** f_new - 3 < c:
        f_new += 1
    return f_new


def back_track(f, c, debug=False):
    # Use the reversed symmetry of the creases around the middle crease
    # to transform c to a crease needing fewer folds, repeat until
    # f = 5, then we can compute the creases w/o building a large vector
    cn = 2 ** f - 1
    mid = 2 ** (f - 1)
    count = 0
    raw_count = 0
    if debug:
        print("before backtrack")
        print(f, c, cn, mid)

    while f > 5:
        if c > cn or c < 1:
            return "error"

        if c == mid:
            # each middle point at 4+ folds will have he same properties
            return 4, 8, (-1) ** count
        elif c > mid:
            c = cn - c + 1
            count += 1

        f -= 1
        cn = 2 ** f - 1
        mid = 2 ** (f - 1)
        raw_count += 1
        if debug:
            print("mid backtrack")
            print(f, c, cn, mid)

    sign = (-1) ** count
    return f, c, sign


def get_crease(f, c, sign=0):
    # Folds the paper f times and calculate each crease.
    # Takes the reversed symmetry in consideration
    # Returns 1-3 creases depending on if they fit in the fold
    count = 2
    creases = np.array([-1, -1, 1])
    middle = np.array([-1])
    while count < f:
        creases = np.concatenate((creases, middle, np.flip(-creases)))
        count += 1

    if sign == 0:  # only for old solver
        ans = array2string(creases[c - 1:c + 2])
    elif sign == 1:
        ans = array2string(creases[c - 1:c + 2])
    elif sign == -1:
        folded_out = np.flip(-creases[:c])
        ans = array2string(folded_out[:3])

    if len(ans) < 1 or len(ans) > 3:
        return "error"

    return ans


def main_old(f, c):
    # Legacy. Get the smallest possible f that contanis c
    # Than compute all creases for f folds and returns the answer
    # Correct but runs on O(2**f), hence very slow for f > 27

    if check_input(f, c) != 0:
        return "error"

    f_nec = get_min_folds(c)
    return get_crease(f_nec, c)


def main_fast(f, c, debug=False):
    # Improves main_old by using the backtracking algorithm before
    # computing the creases. Hence it can calculate creases for
    # f = 5000 in under a second
    # As back_track runs for a single crease and may return a crease
    # that not fits c+1 & c+2 in get_crease it loops until it has all 3 creases

    if check_input(f, c) != 0:
        return "error"

    f = get_min_folds(c)
    ans = ''
    ci = c
    counter = 0
    while len(ans) < 3:
        f_small, c_small, sign = back_track(f, ci, debug)
        if debug:
            print("after backtrack")
            print(f_small, c_small, sign)
        r = get_crease(f_small, c_small, sign)
        if debug:
            print(r)
        ans += r

        if len(ans) == 1:
            ci = c + 1
        elif len(ans) == 2:
            ci = c + 2
        counter += 1
    if debug:
        print(f"needed {counter} tries")
    return ans[:3]


def test_1():
    # Verifies that backtracking method gives same results as exhaustive method
    x = 100000
    c = 10000
    numbers = random.randint(1, x, c)
    correct = 0
    start = time.perf_counter()

    for n in numbers:
        n = int(n)
        a = main_old(26, n)
        b = main_fast(26, n)
        if a != b:
            print(n, a, b)
            print("this was incorrect")
        else:
            correct += 1

    elapsed = time.perf_counter() - start

    if correct == c:
        print("all good")

    print(elapsed)


def test_2():
    # Verifies that backtracking method runs smoothly on multiple large problems
    x = 2**5000
    # numpys random number generator does not handle big numbers
    numbers = [rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x),
              rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x),
              rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x),
              rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x),
              rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x),
              rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x), rd.randint(0, x)]

    start_big = time.perf_counter()
    for n in numbers:
        n = int(n)
        main_fast(5000, n)
    elapsed = time.perf_counter() - start_big
    print(elapsed)


rnum = 2*21 + 13
print(rnum)
print("start main")
print(main_old(30, rnum))
print("finished main")
print("start main2")
print(main_fast(5000, rnum))
print("finished main2")

print("running test_1")
test_1()
print("running test_2")
test_2()
