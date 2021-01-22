from ctypes import windll, byref, sizeof, create_string_buffer, c_short
from ctypes.wintypes import WORD, DWORD


def clear():
    out = windll.kernel32.GetStdHandle(-11)
    flag = DWORD()
    a = windll.kernel32.GetConsoleMode(out, byref(flag))
    flag.value |= 0x4
    b = windll.kernel32.SetConsoleMode(out, flag)
    coo = create_string_buffer(sizeof(c_short) * 2)
    c_short.from_buffer(coo).value = 0
    c_short.from_buffer(coo, sizeof(c_short)).value = 0
    coo = DWORD.from_buffer(coo)
    csi = create_string_buffer(sizeof(c_short) * 10 + sizeof(WORD))
    c = windll.kernel32.GetConsoleScreenBufferInfo(out, csi)
    x = c_short.from_buffer(csi)
    y = c_short.from_buffer(csi, sizeof(c_short))
    written = DWORD()
    d = windll.kernel32.FillConsoleOutputCharacterA(out, ord("\x20"), x.value * y.value, coo, byref(written))
    attr = WORD.from_buffer(csi, sizeof(c_short) * 4)
    e = windll.kernel32.FillConsoleOutputAttribute(out, attr, x.value * y.value, coo, byref(written))
    f = windll.kernel32.SetConsoleCursorPosition(out, coo)
    return a and b and c and d and e and f


if __name__ == '__main__':
    clear()
