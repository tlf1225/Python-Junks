import tkinter as tk


class Runner(tk.Frame):
    def __init__(self, master=None):
        super(Runner, self).__init__(master)
        self.master = master
        self.master.title("Test")
        self.master.geometry("1024x768")
        self.pack()
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.hi_there = tk.Button(self)
        self.create_widgets()

    def create_widgets(self):
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit.pack(side="bottom")

    @staticmethod
    def say_hi():
        print("hi there, everyone!")


if __name__ == '__main__':
    root = tk.Tk()
    app = Runner(master=root)
    app.mainloop()
