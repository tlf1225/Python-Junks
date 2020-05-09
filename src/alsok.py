import tkinter as tk
from json import loads
from urllib.request import urlopen


class App(tk.Frame):
    def __init__(self):
        super(App, self).__init__()
        self.pack()
        self.mainloop()


if __name__ == '__main__':
    App()
    with urlopen("https://api.itsukaralink.jp/livers") as f:
        g = f.info()
        h = loads(f.readline())
        print(h)

    with urlopen("https://api.itsukaralink.jp/events") as e:
        i = e.info()
        j = loads(e.readline())
        print(j)
