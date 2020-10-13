from getpass import getpass
from sys import argv, executable
from time import sleep

# noinspection PyUnresolvedReferences, SpellCheckingInspection
from pywintypes import error as pywin32error
from win32api import CloseHandle, FormatMessage, GetCurrentProcess, GetCurrentThread, GetLastError, ShellExecute, InitiateSystemShutdown, \
    AbortSystemShutdown, GetUserName
from win32comext.shell.shell import IsUserAnAdmin
from win32con import TOKEN_READ, TOKEN_ADJUST_PRIVILEGES, SE_SHUTDOWN_NAME, SE_PRIVILEGE_ENABLED, FORMAT_MESSAGE_ALLOCATE_BUFFER, \
    FORMAT_MESSAGE_FROM_SYSTEM, FORMAT_MESSAGE_IGNORE_INSERTS, LOGON32_LOGON_INTERACTIVE, LOGON32_PROVIDER_DEFAULT
from win32security import LogonUser, ImpersonateLoggedOnUser, OpenProcessToken, OpenThreadToken, LookupPrivilegeValue, AdjustTokenPrivileges, \
    RevertToSelf

if __name__ == '__main__':
    if IsUserAnAdmin():
        print("Admin Mode")
        try:
            Token = OpenProcessToken(GetCurrentProcess(), TOKEN_READ | TOKEN_ADJUST_PRIVILEGES)
            LUV = LookupPrivilegeValue(None, SE_SHUTDOWN_NAME)
            AdjustTokenPrivileges(Token, False, ((LUV, SE_PRIVILEGE_ENABLED),))
            ERROR = FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS, None, GetLastError(),
                                  0, None)
            print(ERROR)
            InitiateSystemShutdown(None, "This is test Text.", 120, False, False)
            sleep(5)
            AbortSystemShutdown(None)
            CloseHandle(Token)
        except pywin32error as e:
            print(e.strerror)
    else:
        try:
            Login = LogonUser(input("Username: ") or GetUserName(), None, getpass("Password: "), LOGON32_LOGON_INTERACTIVE,
                              LOGON32_PROVIDER_DEFAULT)
            ImpersonateLoggedOnUser(Login)
            print("Logged in")
            Token2 = OpenThreadToken(GetCurrentThread(), TOKEN_READ | TOKEN_ADJUST_PRIVILEGES, True)
            LUV2 = LookupPrivilegeValue(None, SE_SHUTDOWN_NAME)
            RES = AdjustTokenPrivileges(Token2, False, ((LUV2, SE_PRIVILEGE_ENABLED),))
            print(RES)
            InitiateSystemShutdown(None, "This is test Text.", 120, False, False)
            sleep(5)
            AbortSystemShutdown(None)
            CloseHandle(Token2)
            RevertToSelf()
            CloseHandle(Login)
        except pywin32error as e:
            print(e.strerror)
            # ExitWindowsEx(0, 0)
            ShellExecute(None, "runas", executable, ' '.join(argv), None, 1)
