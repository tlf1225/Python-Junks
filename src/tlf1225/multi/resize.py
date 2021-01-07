from ctypes import windll


def resize(name, w, h):
    wid = windll.user32.FindWindowW(None, name)
    a = windll.user32.MoveWindow(wid, 0, 0, w, h, False)
    return a


if __name__ in '__main__':
    resize("Minecraft", 1600, 930)
