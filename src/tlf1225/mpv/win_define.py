from ctypes import windll, WINFUNCTYPE, c_int, c_bool, py_object
from ctypes.wintypes import HWND, DWORD, LPCWSTR, LPWSTR, LPDWORD, PLONG, UINT, WPARAM, LPARAM

key = {
    "use_errno": True,
    "use_last_error": True
}

DELEGATE = WINFUNCTYPE(c_bool, HWND, py_object)

FindWindowF = WINFUNCTYPE(HWND, LPCWSTR, LPCWSTR, **key)
FindWindowP = (1, "lpClassName"), (1, "lpWindowName")
# noinspection PyArgumentList
FindWindow = FindWindowF(("FindWindowW", windll.user32), FindWindowP)

FindWindowExF = WINFUNCTYPE(HWND, HWND, HWND, LPCWSTR, LPCWSTR, **key)
# noinspection SpellCheckingInspection
FindWindowExP = (1, "hWndParent"), (1, "hWndChildAfter"), (1, "lpszClass"), (1, "lpszWindow")
# noinspection PyArgumentList
FindWindowEx = FindWindowExF(("FindWindowExW", windll.user32), FindWindowExP)

GetParentF = WINFUNCTYPE(HWND, HWND, **key)
GetParentP = (1, "hWnd"),
# noinspection PyArgumentList
GetParent = GetParentF(("GetParent", windll.user32), GetParentP)

EnumChildWindowsF = WINFUNCTYPE(c_bool, HWND, DELEGATE, py_object, **key)
EnumChildWindowsP = (1, "hWndParent"), (1, "lpEnumFunc"), (1, "lParam")
# noinspection PyArgumentList
EnumChildWindows = EnumChildWindowsF(("EnumChildWindows", windll.user32), EnumChildWindowsP)

EnumWindowsF = WINFUNCTYPE(c_bool, DELEGATE, py_object, **key)
EnumWindowsP = (1, "lpEnumFunc"), (1, "lParam")
# noinspection PyArgumentList
EnumWindows = EnumWindowsF(("EnumWindows", windll.user32), EnumWindowsP)

EnumThreadWindowsF = WINFUNCTYPE(c_bool, DWORD, DELEGATE, py_object, **key)
# noinspection SpellCheckingInspection
EnumThreadWindowsP = (1, "dwThreadId"), (1, "lpfn"), (1, "lParam")
# noinspection PyArgumentList
EnumThreadWindows = EnumThreadWindowsF(("EnumThreadWindows", windll.user32), EnumThreadWindowsP)

GetWindowThreadProcessIdF = WINFUNCTYPE(DWORD, HWND, LPDWORD, **key)
# noinspection SpellCheckingInspection
GetWindowThreadProcessIdP = (1, "hWnd"), (1, "lpdwProcessId")
# noinspection PyArgumentList
GetWindowThreadProcessId = GetWindowThreadProcessIdF(("GetWindowThreadProcessId", windll.user32), GetWindowThreadProcessIdP)

SendMessageTimeoutF = WINFUNCTYPE(PLONG, HWND, UINT, WPARAM, LPARAM, UINT, UINT, LPDWORD, **key)
# noinspection SpellCheckingInspection
SendMessageTimeoutP = (1, "hWnd"), (1, "Msg"), (1, "wParam"), (1, "lParam"), (1, "fuFlags"), (1, "uTimeout"), (2, "lpdwResult")
# noinspection PyArgumentList
SendMessageTimeout = SendMessageTimeoutF(("SendMessageTimeoutW", windll.user32), SendMessageTimeoutP)

GetAnyF = WINFUNCTYPE(c_int, HWND, LPWSTR, c_int, **key)
GetAnyP = (1, "hWnd"), (1, "lpString"), (1, "nMaxCount")
# noinspection PyArgumentList
GetClassName = GetAnyF(("GetClassNameW", windll.user32), GetAnyP)
# noinspection PyArgumentList
GetWindowText = GetAnyF(("GetWindowTextW", windll.user32), GetAnyP)

SetForegroundWindowF = WINFUNCTYPE(c_bool, HWND, **key)
GetWindowTextLengthF = WINFUNCTYPE(c_int, HWND, **key)
GetAnyP2 = (1, "hWnd"),
# noinspection PyArgumentList
SetForegroundWindow = SetForegroundWindowF(("SetForegroundWindow", windll.user32), GetAnyP2)
# noinspection PyArgumentList
GetWindowTextLength = GetWindowTextLengthF(("GetWindowTextLengthW", windll.user32), GetAnyP2)

SetWindowPosF = WINFUNCTYPE(c_bool, HWND, HWND, c_int, c_int, c_int, c_int, UINT, **key)
SetWindowPosP = (1, "hWnd"), (1, "hWndInsertAfter"), (1, "X"), (1, "Y"), (1, "cx"), (1, "cy"), (1, "uFlags")
# noinspection PyArgumentList
SetWindowPos = SetWindowPosF(("SetWindowPos", windll.user32), SetWindowPosP)

GetShellWindowF = WINFUNCTYPE(HWND, **key)
# noinspection PyArgumentList
GetShellWindow = GetShellWindowF(("GetShellWindow", windll.user32), None)

# noinspection SpellCheckingInspection
SWP_NOSIZE = 1
# noinspection SpellCheckingInspection
SWP_NOMOVE = 2

# noinspection SpellCheckingInspection
__all__ = ("SWP_NOMOVE", "SWP_NOSIZE", "DELEGATE", "FindWindow", "FindWindowEx", "GetParent", "EnumWindows", "EnumChildWindows", "EnumThreadWindows",
           "GetWindowThreadProcessId", "SendMessageTimeout", "GetClassName", "GetWindowText", "SetForegroundWindow", "GetWindowTextLength",
           "SetWindowPos", "GetShellWindow", "DWORD", "HWND")
