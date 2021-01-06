# noinspection PyUnresolvedReferences
# from ctypes import windll
from pywintypes import error as win_exception
# noinspection PyUnresolvedReferences
from win32con import HWND_TOPMOST, HWND_NOTOPMOST, SWP_NOMOVE, SWP_NOSIZE, WM_KEYUP, WM_KEYDOWN
from win32gui import FindWindow, FindWindowEx, EnumWindows, EnumChildWindows, GetClassName, GetWindowText, SendMessageTimeout, SetWindowPos, \
    SetForegroundWindow, EnumThreadWindows, SendMessage
from win32process import GetCurrentProcessId, GetWindowThreadProcessId


def enum_info(hwnd: int, param):
    cls, wt = GetClassName(hwnd), GetWindowText(hwnd)
    print("\t" * param + f"H: {hwnd}, C: {cls}, T: {wt}")
    return EnumChildWindows(hwnd, enum_info, param + 1)


def enum_window():
    try:
        EnumWindows(enum_info, 0)
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
            print("\t" * param + f"H: {hwnd}, C: {cls}, T: {wt}")
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


def key_send(ids: int, key: list):
    for i in key:
        SendMessage(ids, WM_KEYDOWN, i, 0)

    for i in key:
        SendMessage(ids, WM_KEYUP, i, 0)


if __name__ == '__main__':
    # print(default_info())
    # print(enum_window())
    res = search_background()
    print(res)
    print(FindWindowEx(res[7], None, "mpv", None))
