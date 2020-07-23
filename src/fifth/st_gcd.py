from math import gcd
from sys import argv


def euclid(alpha=0, beta=0, s_list=None, t_list=None):
    if s_list is None:
        s_list = [1, 0]
    if t_list is None:
        t_list = [0, 1]
    a_to_b = (alpha // beta)
    alpha -= beta * a_to_b
    if alpha == 0:
        return s_list, t_list
    s_list.append(s_list[-2] - s_list[-1] * a_to_b)
    t_list.append(t_list[-2] - t_list[-1] * a_to_b)
    return euclid(beta, alpha, s_list, t_list)


if __name__ == '__main__':
    if len(argv) > 2:
        a = int(argv[1])
        b = int(argv[2])
    else:
        a = 2323
        b = 1717
    ab_gcd = gcd(a, b)
    print(f"a, b = {a}, {b}")
    s, t = euclid(a, b)

    target = s[-1] * a + t[-1] * b
    print(f"gcd_valid = {target == ab_gcd}")
    print(f"gcd_target = {target}")
    print(f"s = {s}")
    print(f"t = {t}")
