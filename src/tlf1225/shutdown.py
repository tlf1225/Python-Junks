from ctypes import windll, create_unicode_buffer, byref, Structure, POINTER
from ctypes.wintypes import DWORD, LONG, HANDLE, PHANDLE, LPWSTR
from os import environ
from sys import argv, executable, stderr
from time import sleep

# noinspection PyUnresolvedReferences
from getpass import getpass


class LuID(Structure):
    _fields_ = [("LowPart", DWORD), ("HighPart", LONG)]


# noinspection SpellCheckingInspection
class LUIDAttributes(Structure):
    _fields_ = [("Luid", LuID), ("Attributes", DWORD)]


class TokenPrivileges(Structure):
    _fields_ = [("PrivilegeCount", DWORD), ("Privileges", POINTER(LUIDAttributes))]


if __name__ == '__main__':
    try:
        CloseHandle = windll.kernel32.CloseHandle
        FormatMessageW = windll.kernel32.FormatMessageW
        GetCurrentProcess = windll.kernel32.GetCurrentProcess
        GetLastError = windll.kernel32.GetLastError
        LocalFree = windll.kernel32.LocalFree

        IsUserAnAdmin = windll.shell32.IsUserAnAdmin
        ShellExecuteW = windll.shell32.ShellExecuteW

        ExitWindowsEx = windll.user32.ExitWindowsEx

        AbortSystemShutdownW = windll.advapi32.AbortSystemShutdownW
        AdjustTokenPrivileges = windll.advapi32.AdjustTokenPrivileges
        ImpersonateLoggedOnUser = windll.advapi32.ImpersonateLoggedOnUser
        InitiateSystemShutdownExW = windll.advapi32.InitiateSystemShutdownExW
        OpenProcessToken = windll.advapi32.OpenProcessToken
        LogonUserW = windll.advapi32.LogonUserW
        LookupPrivilegeValueW = windll.advapi32.LookupPrivilegeValueW
        RevertToSelf = windll.advapi32.RevertToSelf

        # ExitWindowsEx(0, 0)

        if IsUserAnAdmin():
            print("Admin Mode")
        else:
            ShellExecuteW(None, "runas", executable, ' '.join(argv), None, 1)
            exit(0)

        Login = HANDLE()
        # noinspection SpellCheckingInspection
        if LogonUserW(input("UserName: "), environ['COMPUTERNAME'], getpass("Password: "), 4, 0, PHANDLE(Login)):
            ImpersonateLoggedOnUser(Login)
            Token = HANDLE()
            # noinspection SpellCheckingInspection
            luid = LuID()
            if OpenProcessToken(GetCurrentProcess(), 0x28, PHANDLE(Token)):
                if LookupPrivilegeValueW(None, "SE_SHUTDOWN_NAME", byref(luid)):
                    tv = TokenPrivileges()
                    tv.PrivilegeCount = 1
                    tv.Privileges[0].Luid = luid
                    tv.Privileges[0].Attributes = 2
                    if AdjustTokenPrivileges(Token, False, byref(Token), 0, 0, 0):
                        print("SETUP")
                CloseHandle(Token)
            ER = LPWSTR()
            if FormatMessageW(0x1300, None, GetLastError(), 0, byref(ER), 0, None):
                print(ER.value.rstrip())
                LocalFree(ER)
            STD = create_unicode_buffer("This is test Text.")
            if InitiateSystemShutdownExW(None, byref(STD), 120, False, False, 0):
                sleep(1)
                AbortSystemShutdownW(None)
            ER = LPWSTR()
            if FormatMessageW(0x1300, None, GetLastError(), 0, byref(ER), 0, None):
                print(ER.value.rstrip())
                LocalFree(ER)
            RevertToSelf()
            CloseHandle(Login)
        sleep(5)
    except (AttributeError, OSError) as e:
        print(e, file=stderr)
        exit(-1)
