import tkinter as tk
import re

class App:
    oval_description_re = re.compile(r"oval \<(?P<x0>[\-+]?\d+) (?P<y0>[\-+]?\d+) " \
                             r"(?P<x1>\d+) (?P<y1>\d+)\> " \
                             r"(?P<width>\d+) "
                             r"(?P<outline>#[0-9a-fA-F]{6}) " \
                             r"(?P<fill>#[0-9a-fA-F]{6})")
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
        self.text.tag_config("error", background="red", selectbackground="#ff5c77")
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Double-Button-1>", self.canvas_click)
        self.canvas.bind("<Motion>", self.canvas_move)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.oval_creating = False
        self.oval_moving = False

    def start_app(self):
        self.root.mainloop()

    def release(self, event):
        self.oval_creating = False
        self.oval_moving = False
        self.update_text()

    def canvas_click(self, event):
        self.coord_x, self.coord_y = event.x, event.y
        ovals = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if ovals:
            self.oval = ovals[-1]
            self.canvas.tag_raise(self.oval)
            self.oval_moving = True
        else:
            self.oval = self.canvas.create_oval(event.x, event.y, event.x, event.y,
                                               fill="#f0f0f0", outline="#000000", width=2)
            self.oval_creating = True

    def canvas_move(self, event):
        if self.oval_creating:
            x0, y0, x1, y1 = self.coord_x, self.coord_y, event.x, event.y
            self.canvas.coords(self.oval, x0, y0, x1, y1)
        elif self.oval_moving:
            self.canvas.move(self.oval, event.x - self.coord_x, event.y - self.coord_y)
            self.coord_x, self.coord_y = event.x, event.y

    def text_click(self, event):
        self.canvas.delete("all")
        self.text.tag_remove("error", "0.0", tk.END)
        input_description = self.text.get('1.0', 'end-1c').splitlines()
        for i, line in enumerate(input_description):
            match = App.oval_description_re.fullmatch(line)
            if match:
                params = match.groupdict()
                self.canvas.create_oval(params['x0'], params["y0"], params["x1"], params["y1"],
                                        fill=params["fill"], outline=params["outline"], width=int(params["width"]))
            else:
                self.text.tag_add("error", f"{i + 1}.0", f"{i + 1}.end")


    def update_text(self):
        self.text.delete('0.0', tk.END)
        for oval in self.canvas.find_all():
            self.text.insert("end", App.to_text(oval, self.canvas))

    @staticmethod
    def to_text(oval, canvas):
        coords = canvas.coords(oval)
        return f"oval <{round(coords[0])} {round(coords[1])} " \
               f"{round(coords[2])} {round(coords[3])}> " \
               f"{round(float(canvas.itemcget(oval, 'width')))} {canvas.itemcget(oval, 'outline')} " \
               f"{canvas.itemcget(oval, 'fill')}\n"


if __name__ == '__main__':
    graphedit = App()
    graphedit.start_app()