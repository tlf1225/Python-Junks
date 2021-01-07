from code import interact
from itertools import zip_longest
from random import SystemRandom
from re import compile as py_compile


def main(seed=None):
    rand = SystemRandom(seed)

    def reader(prompt):
        temp = input(prompt)
        if temp.startswith(r"//"):
            rp = py_compile(r"[+\-*/]")
            rs = py_compile(r"\s")
            work = rs.sub("", temp[2:].strip())
            if work.startswith("s"):
                rand.seed(int(work[1:]))
                return work[1:]
            data = []
            for x, y in zip_longest(rp.split(work), rp.finditer(work)):
                dice = [int(z) for z in x.split("d") if z]
                if len(dice) == 2:
                    sam = []
                    for i in range(dice[0]):
                        sam.append(rand.randint(1, dice[1]))
                    print(f"{x} = {sam}")
                    data.append(str(sum(sam)))
                    if y:
                        data.append(y.group())
                elif x:
                    data.append(x)
                    if y:
                        data.append(y.group())
                else:
                    data.pop()
            print(data)
            return "".join(data)
        else:
            return temp

    interact(banner="", local=locals(), readfunc=reader, exitmsg="")


if __name__ == '__main__':
    main()
