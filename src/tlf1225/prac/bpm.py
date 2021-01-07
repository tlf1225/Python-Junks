import msvcrt
from code import interact
from math import modf
from time import process_time, perf_counter, monotonic


def time_to_human(now):
    a, b = divmod(now, 86400)  # a = days
    c, d = divmod(b, 3600)  # c = hour
    e, f = divmod(d, 60)  # e = minute
    g, h = modf(f)  # h = seconds, g = micro-seconds
    return int(a), int(c), int(e), int(h), g


def emulate_bpm(bpm=0):
    try:
        tempo = bpm
        c = 0
        while True:
            a = monotonic() + 60 / tempo
            while True:
                b = monotonic()
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'/':
                        tempo -= 1
                    elif key == b'*':
                        tempo += 1
                    elif key == b'c':
                        c = 0
                if b > a:
                    break
            c += 1
            print(f"BPM: {tempo} Beats 32 16 8 4 2 1: {c:3d} {c / 2:3.3f} {c / 4:3.3f} {c / 8:3.3f} {c / 16:3.3f} {c / 32:3.3f}", end="\t\r")
    except KeyboardInterrupt as e:
        print(e)


if __name__ == '__main__':
    print(monotonic())
    print(perf_counter())
    print(process_time())

    print("{0:d}d {1:02d}h {2:02d}m {3:02d}s {4:n}".format(*time_to_human(monotonic())), end="\r")

    interact(local=locals())
