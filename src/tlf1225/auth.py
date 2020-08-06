#!/usr/bin/env python3
import sys
from hashlib import sha3_256

# noinspection PyUnresolvedReferences
import copy
# noinspection PyUnresolvedReferences
import platform

validate = '1e90ce9cb0f0203e2403437c28a97300ac35ab388b3e5b9e411958d3fc3264fe'


# noinspection SpellCheckingInspection
def getpass(prompt="Password: ", echo=False):
    if platform.system() == "Windows":
        import msvcrt
        for x in prompt:
            msvcrt.putwch(x)
        req = ''
        while True:
            # if msvcrt.kbhit():
            #    msvcrt.getwch()
            ch = msvcrt.getwch()
            if u'\x00' <= ch <= u'\x1f':
                break
            req += ch
            if ch in u'\x00\xe0':
                ch = msvcrt.getwch()
                req += ch
            if echo:
                msvcrt.putwch(ch)
        msvcrt.putwch(u'\x0a')
        return sha3_256(req.encode())
    else:
        import termios
        if not echo:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            new = copy.copy(old)
            new[3] &= ~termios.ECHO
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, new)
                return sha3_256(input(prompt).encode())
            except EOFError:
                return ""
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
                print()
        else:
            return sha3_256(input(prompt).encode())


def call():
    print(f"Your info: {platform.release()}")


if __name__ == '__main__':
    # a = input()
    # print([ord(x) for x in a])
    res = getpass(echo=False)
    # pdb.set_trace()
    compare = res.hexdigest()
    print(compare)
    if validate == compare:
        print("OK")
        call()
    else:
        print("Invalid")
    # print([ord(x) for x in res])
    # print([*res])
    # print(res)
