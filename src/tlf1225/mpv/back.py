# noinspection PyUnresolvedReferences
from ctypes import windll
from sys import stderr

# noinspection PyUnresolvedReferences
from pywintypes import error as win_exception
# noinspection PyUnresolvedReferences
from win32con import HWND_TOPMOST, HWND_NOTOPMOST, SWP_NOMOVE, SWP_NOSIZE
from win32gui import FindWindow, FindWindowEx, EnumWindows, EnumChildWindows, GetClassName, GetWindowText, SendMessageTimeout, SetWindowPos, \
    SetForegroundWindow, EnumThreadWindows, GetParent
from win32process import GetCurrentProcessId, GetWindowThreadProcessId


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
        return result
    except win_exception as e:
        print(e.strerror)


def default_info():
    pro = FindWindow("Progman", "Program Manager")
    shell = FindWindowEx(pro, None, "SHELLDLL_DefView", None)
    view = FindWindowEx(shell, None, "SysListView32", "FolderView")
    return pro, shell, view


def search_background():
    # pro = windll.user32.GetShellWindow()
    pro = FindWindow("Progman", "Program Manager")
    SendMessageTimeout(pro, 0x52C, None, None, 0, 1000)
    tid, pid = GetWindowThreadProcessId(pro)
    result = ()
    try:
        def worker(hwnd: int, param):
            nonlocal result
            cls, wt = GetClassName(hwnd), GetWindowText(hwnd)
            print("\t" * param + f"H: {hwnd}, C: {cls}, T: {wt}", file=stderr)
            if cls == "WorkerW":
                shell = FindWindowEx(hwnd, None, "SHELLDLL_DefView", None)
                if shell:
                    view = FindWindowEx(shell, None, "SysListView32", "FolderView")
                    if view:
                        window = FindWindowEx(None, hwnd, "WorkerW", None)
                        result = pid, tid, cls, wt, hwnd, shell, view, window
                        return False
            return True

        EnumThreadWindows(tid, worker, 0)
    except win_exception as e:
        print(e.strerror)

    return result


# noinspection PyTypeChecker, SpellCheckingInspection
def topmost(hwnd_value: int):
    def finder(hwnd: int, lp):
        nonlocal hwnd_value
        tid, pid = GetWindowThreadProcessId(hwnd)
        if pid == lp:
            SetForegroundWindow(hwnd)
            SetWindowPos(hwnd, hwnd_value, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)

    EnumWindows(finder, GetCurrentProcessId())


def show_enum_windows(enum=None, c=0):
    for i in enum:
        if isinstance(i, tuple):
            show_enum_windows(i, c + 1)
        else:
            print('\t' * (c - 1) + f"H: {i}, C: {GetClassName(i)}, T: {GetWindowText(i)}")


if __name__ == '__main__':
    # print(default_info())
    show_enum_windows(enum_windows())
    res = search_background()
    print(res)
    print(FindWindowEx(res[7], None, "mpv", None))
