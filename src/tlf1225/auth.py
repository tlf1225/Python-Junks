#!/usr/bin/env python3
from copy import copy
from hashlib import sha3_256
from pdb import set_trace
from platform import release, system
from sys import stdin

from pyotp.totp import TOTP
from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardData, CloseClipboard, CF_TEXT

validate = '1e90ce9cb0f0203e2403437c28a97300ac35ab388b3e5b9e411958d3fc3264fe'


# noinspection SpellCheckingInspection
def getpass(prompt="Password: ", echo=False):
    if system() == "Windows":
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
            fd = stdin.fileno()
            old = termios.tcgetattr(fd)
            new = copy(old)
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
    print(f"Your info: {release()}")


# noinspection SpellCheckingInspection
def two_auth(key="HQKESDOB2WJO2USF7NWIO6GMH4"):
    """
    HQKESDOB2WJO2USF7NWIO6GMH4
    " RATE_LIMIT 3 30 1602326446
    " DISALLOW_REUSE 53410882
    " TOTP_AUTH
    13479604
    12761979
    29247964
    69516535
    14451533
    """

    key = TOTP(key)
    current = key.now().encode()
    OpenClipboard()
    EmptyClipboard()
    SetClipboardData(CF_TEXT, current)
    CloseClipboard()


if __name__ == '__main__':
    two_auth()

    set_trace()

    a = input()
    print([ord(x) for x in a])

    res = getpass(echo=False)

    compare = res.hexdigest()
    print(compare)

    if validate == compare:
        print("OK")
        call()
    else:
        print("Invalid")
