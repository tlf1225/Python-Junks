from ctypes import windll

# noinspection SpellCheckingInspection
ES_AWAYMODE_REQUIRED = 0x00000040
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
ES_SYSTEM_REQUIRED = 0x00000001

HWND_BROADCAST = 0xffff
# noinspection SpellCheckingInspection
WM_SYSCOMMAND = 0x0112
# noinspection SpellCheckingInspection
SC_MONITORPOWER = 0xF170

if __name__ == '__main__':
    windll.kernel32.SetThreadExecutionState(ES_AWAYMODE_REQUIRED | ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED | ES_CONTINUOUS)
    print("START")
    while True:
        try:
            print(input())
            windll.user32.SendMessageA(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)
        except EOFError as e:
            print(e)
            break
    windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    print("EXIT")
