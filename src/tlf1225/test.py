from ctypes import *
from ctypes.wintypes import *
from os.path import basename
from sys import exit, argv

try:
    MAX_PATH = 260
    PROCESS_TERMINATE = 0x0001
    PROCESS_QUERY_INFORMATION = 0x0400
    HWND_TOPMOST = HWND(-1)
    # noinspection SpellCheckingInspection
    HWND_NOTOPMOST = HWND(-2)
    # noinspection SpellCheckingInspection
    SWP_NOSIZE = 0x1
    # noinspection SpellCheckingInspection
    SWP_NOMOVE = 0x2
    WS_EX_TOPMOST = 0x8
    # noinspection SpellCheckingInspection
    WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)

    # noinspection SpellCheckingInspection
    PSAPI = windll.psapi
    KERNEL32 = windll.kernel32
    USER32 = windll.user32

    EnumProcesses = PSAPI.EnumProcesses
    EnumProcesses.restype = BOOL
    # noinspection SpellCheckingInspection
    EnumProcesses.argtypes = (LPDWORD, DWORD, LPDWORD)

    GetProcessImageFileName = PSAPI.GetProcessImageFileNameW
    GetProcessImageFileName.restype = DWORD
    # noinspection SpellCheckingInspection
    GetProcessImageFileName.argtypes = (HANDLE, LPWSTR, DWORD)

    OpenProcess = KERNEL32.OpenProcess
    OpenProcess.restype = HANDLE
    # noinspection SpellCheckingInspection
    OpenProcess.argtypes = (DWORD, BOOL, DWORD)

    TerminateProcess = KERNEL32.TerminateProcess
    TerminateProcess.restype = BOOL
    # noinspection SpellCheckingInspection
    TerminateProcess.argtypes = (HANDLE, UINT)

    CloseHandle = KERNEL32.CloseHandle
    CloseHandle.restype = BOOL
    # noinspection SpellCheckingInspection
    CloseHandle.argtypes = (HANDLE,)

    SetWindowPos = USER32.SetWindowPos
    SetWindowPos.restype = BOOL
    # noinspection SpellCheckingInspection
    SetWindowPos.argtypes = (HWND, HWND, INT, INT, INT, INT, UINT)

    EnumWindows = USER32.EnumWindows
    EnumWindows.restype = BOOL
    # noinspection SpellCheckingInspection
    EnumWindows.argtypes = (WNDENUMPROC, LPARAM)

    EnumThreadWindows = USER32.EnumThreadWindows
    EnumThreadWindows.restype = BOOL
    # noinspection SpellCheckingInspection
    EnumThreadWindows.argtypes = (DWORD, WNDENUMPROC, LPARAM)

    GetWindowThreadProcessId = USER32.GetWindowThreadProcessId
    GetWindowThreadProcessId.restype = DWORD
    # noinspection SpellCheckingInspection
    GetWindowThreadProcessId.argtypes = (HWND, LPDWORD)

    GetWindowText = USER32.GetWindowTextW
    GetWindowText.restype = INT
    # noinspection SpellCheckingInspection
    GetWindowText.argtypes = (HWND, LPWSTR, INT)


    def perform(name=None, pid=None, flag=False):
        def worker(hwnd, lp):
            res = DWORD()
            # noinspection PyTypeChecker
            if GetWindowThreadProcessId(hwnd, byref(res)) \
                    and EnumThreadWindows(res, WNDENUMPROC(worker), lp) and res.value == lp:
                text = create_unicode_buffer(1024)
                GetWindowText(hwnd, text, sizeof(text))
                if len(text.value) > 0:
                    if text.value.find(name) > 0:
                        print(text.value)
                        if flag:
                            SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
                        else:
                            SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
                        return False
            return True

        # noinspection PyTypeChecker
        EnumWindows(WNDENUMPROC(worker), pid)

except OSError as e:
    print(e.strerror)
    exit(-1)


# noinspection PyCallingNonCallable, PyTypeChecker, SpellCheckingInspection
def main(args=None):
    pids = (DWORD * 1024)()
    cb = sizeof(pids)
    bret = DWORD()
    if EnumProcesses(cast(pids, POINTER(DWORD)), cb, byref(bret)):
        for index in range(bret.value // sizeof(DWORD)):
            pid = pids[index]
            process = OpenProcess(PROCESS_TERMINATE | PROCESS_QUERY_INFORMATION, False, pid)
            if process:
                image_file_name = create_unicode_buffer(MAX_PATH)
                if GetProcessImageFileName(process, image_file_name, MAX_PATH) > 0:
                    filename = basename(image_file_name.value)
                    if filename == args[0]:
                        perform(filename, pid, True)
                    if len(args) > 2:
                        TerminateProcess(process, 1)
                CloseHandle(process)


if __name__ == '__main__':
    main(argv[1::])
