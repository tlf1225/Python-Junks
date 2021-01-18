from ctypes import windll, WINFUNCTYPE, c_int, c_bool, py_object
# noinspection PyUnresolvedReferences
from ctypes.wintypes import HWND, DWORD

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
