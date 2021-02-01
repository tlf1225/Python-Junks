from ctypes import windll, byref, c_short, c_void_p, Structure
from ctypes.wintypes import WORD, DWORD
from os import pipe


class COORD(Structure):
    _fields_ = (
        ("x", c_short),
        ("y", c_short)
    )


class SmallRect(Structure):
    _fields_ = (
        ("left", c_short),
        ("top", c_short),
        ("right", c_short),
        ("bottom", c_short)
    )


class ConsoleScreenBufferInfo(Structure):
    _fields_ = (
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", WORD),
        ("srWindow", SmallRect),
        ("dwMaximumWindowSize", COORD)
    )


def clear():
    out = windll.kernel32.GetStdHandle(-11)
    flag = DWORD()
    a = windll.kernel32.GetConsoleMode(out, byref(flag))
    flag.value |= 0x4
    b = windll.kernel32.SetConsoleMode(out, flag)
    coo = COORD()
    csi = ConsoleScreenBufferInfo()
    c = windll.kernel32.GetConsoleScreenBufferInfo(out, byref(csi))
    x = csi.dwSize.x
    y = csi.dwSize.y
    written = DWORD()
    d = windll.kernel32.FillConsoleOutputCharacterA(out, ord("\x20"), x * y, coo, byref(written))
    e = windll.kernel32.FillConsoleOutputAttribute(out, csi.wAttributes, x * y, coo, byref(written))
    f = windll.kernel32.SetConsoleCursorPosition(out, coo)
    return a and b and c and d and e and f


def work():
    a = COORD()
    a.x = 120
    a.y = 30

    stdin, stdout = pipe()
    con = c_void_p()
    windll.kernel32.CreatePseudoConsole(a, stdin, stdout, 0, byref(con))
    print(con)
    windll.kernel32.ClosePseudoConsole(con)


if __name__ == '__main__':
    clear()
    # work()
