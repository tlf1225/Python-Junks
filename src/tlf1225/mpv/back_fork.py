from ctypes import byref, create_unicode_buffer
from sys import stderr

# from tlf1225.mpv.back_define import *
from tlf1225.mpv.win_define import *


@DELEGATE
def enum_parent(hwnd: HWND, param: list) -> bool:
    param.append(hwnd)
    return True


@DELEGATE
def enum_child(hwnd: HWND, param: tuple = (int, list)) -> bool:
    if GetParent(hwnd) == param[0]:
        param[1].append(hwnd)
    else:
        child = []
        EnumChildWindows(hwnd, enum_child, (hwnd, child))
        if child:
            param[1].append((hwnd, tuple(child)))
    return True


@DELEGATE
def enum_thread(hwnd: HWND, param: tuple = (int, list)) -> bool:
    child = []
    EnumChildWindows(hwnd, enum_child, (hwnd, child))
    if child:
        param[1].append((hwnd, tuple(child)))
    else:
        param[1].append(hwnd)
    return True


def enum_windows() -> tuple:
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


def search_background() -> tuple:
    pro = GetShellWindow()
    # noinspection SpellCheckingInspection
    """ pro = FindWindow("Progman", "Program Manager") """
    x = DWORD()
    SendMessageTimeout(pro, 0x52C, 0, 0, 0, 1000, byref(x))
    pid = DWORD()
    tid = GetWindowThreadProcessId(pro, byref(pid))
    result = [(pid.value, tid)]
    child = []
    EnumThreadWindows(tid, enum_thread, (pro, child))
    result.append(tuple(child))
    return tuple(result)


def query_info(quest: int) -> tuple:
    cls = create_unicode_buffer(256)
    GetClassName(quest, cls, 256)
    win_len = GetWindowTextLength(quest)
    if win_len > 0:
        win_len += 1
        wt = create_unicode_buffer(win_len)
        GetWindowText(quest, wt, win_len)
        return cls.value, wt.value
    else:
        return cls.value, ""


def topmost(enum: tuple = enum_windows(), c: int = 0, hwnd_value: int = -1, cl: str = None, wtx: str = None):
    for i in enum:
        if isinstance(i, tuple):
            topmost(i, c + 1, hwnd_value, cl, wtx)
        else:
            cls, wt = query_info(i)
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
            cls, wt = query_info(i)
            if cl and cls.find(cl) >= 0 or wtx and wt.find(wtx) >= 0:
                print(f"Found {i}, {cls}, {wt}")


def show_enum_windows(enum: tuple = enum_windows(), c: int = 0):
    for i in enum:
        if isinstance(i, tuple):
            show_enum_windows(i, c + 1)
        else:
            cls, wt = query_info(i)
            print('\t' * (c - 1) + f"H: {i}, C: {cls}, T: {wt}", file=stderr)
    else:
        print('-' * 4 * (c - 1), file=stderr)


if __name__ == '__main__':
    show_enum_windows()
    print(search_background(), file=stderr)
