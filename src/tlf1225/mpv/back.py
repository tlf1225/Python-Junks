from sys import stderr

# noinspection PyUnresolvedReferences
from pywintypes import error as win_exception
from win32con import SWP_NOMOVE, SWP_NOSIZE
from win32gui import FindWindow, EnumWindows, EnumChildWindows, GetClassName, GetWindowText, SendMessageTimeout, SetWindowPos, \
    SetForegroundWindow, EnumThreadWindows, GetParent
from win32process import GetWindowThreadProcessId


def enum_parent(hwnd: int, param: list):
    param.append(hwnd)
    return True


def enum_child(hwnd: int, param: tuple = (int, list)):
    if GetParent(hwnd) == param[0]:
        param[1].append(hwnd)
    else:
        child = []
        EnumChildWindows(hwnd, enum_child, (hwnd, child))
        if child:
            param[1].append((hwnd, tuple(child)))
    return True


def enum_windows():
    try:
        parent = []
        EnumWindows(enum_parent, parent)
        result = []
        for i in parent:
            child = []
            EnumChildWindows(i, enum_child, (i, child))
            if child:
                result.append((i, tuple(child)))
            else:
                result.append(i)
        return tuple(result)
    except win_exception as e:
        print(e.strerror)


def search_background():
    # pro = windll.user32.GetShellWindow()
    pro = FindWindow("Progman", "Program Manager")
    SendMessageTimeout(pro, 0x52C, None, None, 0, 1000)
    tid, pid = GetWindowThreadProcessId(pro)
    result = [(pid, tid), []]
    try:
        EnumThreadWindows(tid, enum_child, (-1, result[1]))
    except win_exception as e:
        print(e.strerror)

    return result


# noinspection SpellCheckingInspection
def topmost(enum: tuple = enum_windows(), c: int = 0, hwnd_value: int = -1, cl: str = None, wtx: str = None):
    for i in enum:
        if isinstance(i, tuple):
            topmost(i, c + 1, hwnd_value, cl, wtx)
        else:
            cls, wt = GetClassName(i), GetWindowText(i)
            if cl and cls.find(cl) >= 0 or wtx and wt.find(wtx) >= 0:
                print(f"Found {i}")
                SetForegroundWindow(i)
                SetWindowPos(i, hwnd_value, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
                break


def search(enum: tuple = enum_windows(), c: int = 0, cl: str = None, wtx: str = None):
    for i in enum:
        if isinstance(i, tuple):
            search(i, c + 1, cl, wtx)
        else:
            cls, wt = GetClassName(i), GetWindowText(i)
            if cl and cls.find(cl) >= 0 or wtx and wt.find(wtx) >= 0:
                print(f"Found {i}, {cls}, {wt}")


def show_enum_windows(enum: tuple = enum_windows(), c: int = 0):
    for i in enum:
        if isinstance(i, tuple):
            show_enum_windows(i, c + 1)
        else:
            print('\t' * (c - 1) + f"H: {i}, C: {GetClassName(i)}, T: {GetWindowText(i)}", file=stderr)
    else:
        print('-' * 4 * (c - 1), file=stderr)


if __name__ == '__main__':
    show_enum_windows()
    print(search_background(), file=stderr)
