from code import interact
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


def euler(alpha):
    return (x for x in range(1, alpha) if gcd(x, alpha) == 1)


def fermat_tool():
    def fermat(integer, power, count, base):
        for i in range(count):
            integer = (integer ** power) % base
            # yield integer
        return integer

    def calc(base, *calc_list):
        multiply = 1
        for i in calc_list:
            if isinstance(i, int):
                multiply *= i
        return multiply % base

    return fermat, calc


# f, g = fermat_tool()
# g(127, list(f(5, 2, 6, 127))[-1], list(f(5, 2, 5, 127))[-1], 5)


def ab_tool(calc=lambda x, alpha, beta, n: x ** 2 + ((alpha + beta) % n) * x + (alpha * beta) % n, n=7):
    for i in range(n):
        for j in range(n):
            for k in range(n):
                print(f"x={i},a={j},b={k}")
                d = calc(i, j, k, n)
                print(f"{i}*x^2+{(j + k) % n}*x+{(j * k) % n}={d % n}")
                # print(f"既約: {j % n == 0 or k % n == 0}")


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
    interact(banner="GCD", local=locals(), exitmsg="Exit")
