from ctypes import create_unicode_buffer, windll
from os.path import basename
from sys import argv

# noinspection PyUnresolvedReferences, SpellCheckingInspection
from pywintypes import error as pywin32error
from win32api import CloseHandle, OpenProcess
# noinspection PyUnresolvedReferences
from win32con import MAX_PATH, PROCESS_TERMINATE, PROCESS_QUERY_INFORMATION, HWND_TOPMOST, HWND_NOTOPMOST, SWP_NOSIZE, SWP_NOMOVE, WS_EX_TOPMOST
from win32gui import EnumWindows, EnumThreadWindows, SetWindowPos, GetWindowText
from win32process import EnumProcesses, TerminateProcess, GetWindowThreadProcessId


def perform(name=None, pid=None, flag=False):
    def worker(hwnd, lp):
        tid, pid2 = GetWindowThreadProcessId(hwnd)
        EnumThreadWindows(pid2, worker, lp)
        if pid2 == lp:
            text = GetWindowText(hwnd)
            if text.find(name) > 0:
                if flag:
                    SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
                else:
                    SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
                return False
        return True

    EnumWindows(worker, pid)


def main(args=None):
    for pid in EnumProcesses():
        try:
            process = OpenProcess(PROCESS_TERMINATE | PROCESS_QUERY_INFORMATION, False, pid)
            image_file_name = create_unicode_buffer(MAX_PATH)
            if windll.psapi.GetProcessImageFileNameW(process.handle, image_file_name, MAX_PATH) > 0:
                filename = basename(image_file_name.value)
                if filename == args[0]:
                    perform(filename, pid, True)
                if len(args) > 2:
                    TerminateProcess(process, 1)
            CloseHandle(process)
        except pywin32error as e:
            print(e)


if __name__ == '__main__':
    main(argv[1::])
