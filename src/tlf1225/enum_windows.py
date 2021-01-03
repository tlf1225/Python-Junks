# noinspection PyUnresolvedReferences
from pywintypes import error as win_exception
# noinspection PyUnresolvedReferences
from win32con import HWND_TOPMOST, HWND_NOTOPMOST, SWP_NOMOVE, SWP_NOSIZE
from win32gui import FindWindow, FindWindowEx, EnumWindows, EnumChildWindows, GetClassName, GetWindowText, SendMessageTimeout, SetWindowPos, \
    SetForegroundWindow, EnumThreadWindows
from win32process import GetCurrentProcessId, GetWindowThreadProcessId


def enum_window():
    try:
        def test(hwnd, param):
            cls, wt = GetClassName(hwnd), GetWindowText(hwnd)
            print("\t" * param + f"H: {hwnd}, C: {cls}, T: {wt}")
            return EnumChildWindows(hwnd, test, param + 1)

        EnumWindows(test, 0)
    except win_exception as e:
        print(e.strerror)


def default_info():
    pro = FindWindow("Progman", "Program Manager")
    shell = FindWindowEx(pro, None, "SHELLDLL_DefView", None)
    view = FindWindowEx(shell, None, "SysListView32", "FolderView")
    return pro, shell, view


def search_background():
    pro = FindWindow("Progman", "Program Manager")
    SendMessageTimeout(pro, 0x52C, None, None, 0, 1000)
    tid, pid = GetWindowThreadProcessId(pro)
    result = None
    try:
        def test(hwnd, param):
            nonlocal result
            cls, wt = GetClassName(hwnd), GetWindowText(hwnd)
            print("\t" * param + f"H: {hwnd}, C: {cls}, T: {wt}")
            if cls == "WorkerW":
                shell = FindWindowEx(hwnd, None, "SHELLDLL_DefView", None)
                if shell:
                    view = FindWindowEx(shell, None, "SysListView32", "FolderView")
                    if view:
                        worker = FindWindowEx(None, hwnd, "WorkerW", None)
                        result = pid, tid, cls, wt, hwnd, shell, view, worker
                        return False
            return True

        EnumThreadWindows(tid, test, 0)
    except win_exception as e:
        print(e.strerror)

    return result


# noinspection PyTypeChecker, SpellCheckingInspection
def topmost(hwnd_value):
    def finder(hwnd, lp):
        tid, pid = GetWindowThreadProcessId(hwnd)
        if pid == lp:
            SetForegroundWindow(hwnd)
            SetWindowPos(hwnd, hwnd_value, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)

    EnumWindows(finder, GetCurrentProcessId())


if __name__ == '__main__':
    # print(default_info())
    # print(enum_window())
    print(search_background())
