from math import gcd
from sys import argv

if __name__ == '__main__':
    s = [1, 0]
    t = [0, 1]
    if len(argv) > 2:
        oa = int(argv[1])
        ob = int(argv[2])
    else:
        oa = 2323
        ob = 1717
    ab_gcd = gcd(oa, ob)
    a = oa
    b = ob
    print(f"a, b = {a}, {b}")
    while True:
        temp = b
        work = (a // b)
        b = a - b * work
        a = temp
        if b == 0:
            break

        print(f"a, b = {a}, {b}")

        s.append(s[len(s) - 2] - s[len(s) - 1] * work)
        t.append(t[len(t) - 2] - t[len(t) - 1] * work)

    target = s[-1] * oa + t[-1] * ob
    print(f"gcd_valid = {target == ab_gcd}")
    print(f"gcd_target = {target}")
    print(f"s = {s}")
    print(f"t = {t}")
