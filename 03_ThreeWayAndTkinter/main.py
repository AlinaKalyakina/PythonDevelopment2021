
import random

import tkinter as tk


class Game15():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Пятнашки")
        # сделаем, чтобы колоночки и ряды масштабровались одинаково
        self.window.rowconfigure(0, weight=1, uniform="row_gr")
        for i in range(4):
            self.window.rowconfigure(i + 1, weight=1, uniform="row_gr")
            self.window.columnconfigure(i, weight=1, uniform="col_gr")

        self.new_button = tk.Button(self.window, text="New", command=self.new_click)
        self.new_button.grid(column=0, row=0, columnspan=2)
        self.exit_button = tk.Button(self.window, text="Exit", command=self.exit)
        self.exit_button.grid(column=2, row=0, columnspan=2)
        self.numbers = tuple((tk.Button(self.window, text=str(i+1), command=self.number_click(i)) for i in range(15)))
        self.new_click()

    def new_click(self):
        self.buttons_order = list(range(15))
        random.shuffle(self.buttons_order)
        # пустота
        self.buttons_order.append(None)
        self.place_buttons()

    def exit(self):
        self.window.destroy()

    def place_buttons(self):
        for i, button_id in enumerate(self.buttons_order):
            if button_id is None:
                continue
            self.numbers[button_id].grid(column=i % 4, row=1 + i // 4, sticky=tk.NSEW)

    def number_click(self, n):
        def move():
            n_pos = self.buttons_order.index(n)
            n_y, n_x = divmod(n_pos, 4)
            none_coord = self.buttons_order.index(None)
            none_y, none_x = divmod(none_coord, 4)
            if n_x == none_x and abs(n_y-none_y) == 1  or abs(n_x - none_x) == 1 and n_y == none_y:
                self.buttons_order[n_pos], self.buttons_order[none_coord] = \
                    self.buttons_order[none_coord], self.buttons_order[n_pos]
            self.place_buttons()

        return move


    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    game = Game15()
    game.run()