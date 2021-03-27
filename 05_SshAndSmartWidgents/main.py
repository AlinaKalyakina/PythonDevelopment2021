import tkinter as tk


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph Edit")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.frame = tk.Frame(self.root)
        self.frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=5)

        self.text = tk.Text(self.frame)
        self.text.grid(row=0, column=0, sticky=tk.NSEW)
        self.canvas = tk.Canvas(self.frame)
        self.canvas.grid(row=0, column=1, sticky=tk.NSEW)

        self.text.bind("<KeyRelease>", self.text_click)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Double-Button-1>", self.canvas_click)
        self.canvas.bind("<Motion>", self.canvas_click)

    def start_app(self):
        self.root.mainloop()

    def canvas_click(self, event):
        pass

    def text_click(self, event):
        pass


if __name__ == '__main__':
    graphedit = App()
    graphedit.start_app()