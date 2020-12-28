# noinspection PyUnresolvedReferences
from pywintypes import error as win_exception
# noinspection PyUnresolvedReferences
from win32con import HWND_TOPMOST, HWND_NOTOPMOST, SWP_NOMOVE, SWP_NOSIZE
from win32gui import FindWindow, FindWindowEx, EnumWindows, EnumChildWindows, GetClassName, GetWindowText, SendMessageTimeout, SetWindowPos, \
    SetForegroundWindow
from win32process import GetCurrentProcessId, GetWindowThreadProcessId


def search_background():
    result = ()
    try:
        def test(a, b):
            nonlocal result
            cls = GetClassName(a)
            wt = GetWindowText(a)
            print("\t" * b + f"H: {a}, C: {cls}, T: {wt}")
            if cls == "WorkerW":
                shell = FindWindowEx(a, None, "SHELLDLL_DefView", None)
                if shell:
                    view = FindWindowEx(shell, None, "SysListView32", "FolderView")
                    if view:
                        worker = FindWindowEx(None, a, "WorkerW", None)
                        result = (cls, wt, a, shell, view, worker)
                        return False
            return EnumChildWindows(a, test, b + 1)

        EnumWindows(test, 0)
    except win_exception as e:
        print(e.strerror)

    return result


def default_background():
    pro = FindWindow("Progman", "Program Manager")
    shell = FindWindowEx(pro, None, "SHELLDLL_DefView", None)
    view = FindWindowEx(shell, None, "SysListView32", "FolderView")
    SendMessageTimeout(pro, 0x52C, None, None, 0, 1000)
    return view


# noinspection PyTypeChecker, SpellCheckingInspection
def topmost(hwnd_value):
    def finder(hwnd, lp):
        tid, pid = GetWindowThreadProcessId(hwnd)
        if pid == lp:
            SetWindowPos(hwnd, hwnd_value, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
            SetForegroundWindow(hwnd)

    EnumWindows(finder, GetCurrentProcessId())


if __name__ == '__main__':
    print(default_background())
    print(search_background())
