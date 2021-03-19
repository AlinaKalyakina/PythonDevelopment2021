import re
import tkinter as tk
from tkinter.messagebox import showinfo


class Application(tk.Frame):
    def __init__(self, master=None, title="Application", **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky=tk.NSEW)
        self.createWidgets()

    def __getattr__(self, attr):
        def widget_constructor(attr, root):
            def widget_class_wrapper(widget_class, description_str, **kwargs):
                description = Application.parse_description(description_str)

                class DummyWidget(widget_class):
                    def __init__(self, root, **kwargs):
                        super().__init__(root, **kwargs)
                        self.grid(row=description['row'],
                                  column=description['col'],
                                  rowspan=description['rowspan'] + 1,
                                  columnspan=description['colspan'] + 1,
                                  sticky=description['sticky'])
                        root.columnconfigure(description['col'], weight=description['col_weight'])
                        root.rowconfigure(description['row'], weight=description['row_weight'])

                    def __getattr__(self, sub_widget_name):
                        return widget_constructor(sub_widget_name, self)

                setattr(root, attr, DummyWidget(root, **kwargs))
            return widget_class_wrapper
        return widget_constructor(attr, self)

    @staticmethod
    def parse_description(description):
        default_dict = {'row': "None", 'row_weight': "1", 'col': "None", 'col_weight': "1", 'colspan': "0", 'sticky': 'NEWS', "rowspan": "0"}

        description_dict = re.match(
            r"(?P<row>\d+)(?:\.(?P<row_weight>\d+))?(?:\+(?P<rowspan>\d+))?:(?P<col>\d+)(?:\.(?P<col_weight>\d+))?(?:\+(?P<colspan>\d+))?(?:\/(?P<sticky>\w+))?",
            description).groupdict()

        for key, item in default_dict.items():
            if description_dict[key] is None:
                description_dict[key] = item

        return {key: (eval(value) if key != 'sticky' else value) for key, value in description_dict.items()}


class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))


app = App(title="Sample application")
app.mainloop()