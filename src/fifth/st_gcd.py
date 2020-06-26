from math import gcd

if __name__ == '__main__':
    s = [1, 0]
    t = [0, 1]
    oa = 2323
    ob = 1717
    ab_gcd = gcd(2323, 1717)
    a = oa
    b = ob

    while True:
        temp = b
        work = (a // b)
        b = a - b * work
        a = temp
        if b == 0:
            break

        print(f"{a} {b}")

        s.append(s[len(s) - 2] - s[len(s) - 1] * work)
        t.append(t[len(t) - 2] - t[len(t) - 1] * work)

    target = s[-1] * oa + t[-1] * ob
    print(target == ab_gcd)
    print(target)
    print(s)
    print(t)
