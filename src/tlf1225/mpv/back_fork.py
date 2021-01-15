from ctypes import windll, byref, WINFUNCTYPE, c_int, c_bool, py_object, create_unicode_buffer
from ctypes.wintypes import HWND, DWORD
from sys import stderr

DELEGATE = WINFUNCTYPE(c_bool, HWND, py_object)

GetParent = windll.user32.GetParent
EnumChildWindows = windll.user32.EnumChildWindows
# noinspection SpellCheckingInspection
EnumChildWindows.argtypes = (c_int, DELEGATE, py_object)
EnumWindows = windll.user32.EnumWindows
# noinspection SpellCheckingInspection
EnumWindows.argtypes = (DELEGATE, py_object)
EnumThreadWindows = windll.user32.EnumThreadWindows
# noinspection SpellCheckingInspection
EnumThreadWindows.argtypes = (c_int, DELEGATE, py_object)
GetWindowThreadProcessId = windll.user32.GetWindowThreadProcessId
SendMessageTimeout = windll.user32.SendMessageTimeoutW
GetClassName = windll.user32.GetClassNameW
GetWindowText = windll.user32.GetWindowTextW
SetForegroundWindow = windll.user32.SetForegroundWindow
SetWindowPos = windll.user32.SetWindowPos
FindWindow = windll.user32.FindWindowW
FindWindowEx = windll.user32.FindWindowExW
GetShellWindow = windll.user32.GetShellWindow
# noinspection SpellCheckingInspection
SWP_NOSIZE = 1
# noinspection SpellCheckingInspection
SWP_NOMOVE = 2


def enum_parent(hwnd: HWND, param: list) -> bool:
    param.append(hwnd)
    return True


def enum_child(hwnd: HWND, param: tuple = (int, list)) -> bool:
    if GetParent(hwnd) == param[0]:
        param[1].append(hwnd)
    else:
        child = []
        # noinspection PyTypeChecker
        EnumChildWindows(hwnd, DELEGATE(enum_child), (hwnd, child))
        if child:
            param[1].append((hwnd, tuple(child)))
    return True


def enum_thread(hwnd: HWND, param: tuple = (int, list)) -> bool:
    child = []
    # noinspection PyTypeChecker
    EnumChildWindows(hwnd, DELEGATE(enum_child), (hwnd, child))
    if child:
        param[1].append((hwnd, tuple(child)))
    else:
        param[1].append(hwnd)
    return True


def enum_windows() -> tuple:
    parent = []
    # noinspection PyTypeChecker
    EnumWindows(DELEGATE(enum_parent), parent)
    result = []
    for i in parent:
        child = []
        # noinspection PyTypeChecker
        EnumChildWindows(i, DELEGATE(enum_child), (i, child))
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
    SendMessageTimeout(pro, 0x52C, None, None, 0, 1000, byref(x))
    pid = DWORD()
    tid = GetWindowThreadProcessId(pro, byref(pid))
    result = [(pid.value, tid)]
    child = []
    # noinspection PyTypeChecker
    EnumThreadWindows(tid, DELEGATE(enum_thread), (pro, child))
    result.append(tuple(child))
    return tuple(result)


def query_info(quest: int, n: int = 256) -> tuple:
    result = []
    cls, wt = create_unicode_buffer(n), create_unicode_buffer(n)
    GetClassName(quest, byref(cls), n)
    GetWindowText(quest, byref(wt), n)
    cls, wt = cls.value, wt.value
    result.append(cls)
    result.append(wt)
    return tuple(result)


# noinspection SpellCheckingInspection
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
