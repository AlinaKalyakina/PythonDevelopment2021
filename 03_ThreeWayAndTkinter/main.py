import random

import tkinter as tk
import tkinter.messagebox

class Game15():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Пятнашки")
        # сделаем, чтобы колоночки и ряды масштабровались одинаково
        for i in range(4):
            self.window.rowconfigure(i, weight=1, uniform="row_gr")
            self.window.columnconfigure(i, weight=1, uniform="col_gr")
        self.window.rowconfigure(4, weight=1, uniform="row_gr")

        self.new_button = tk.Button(self.window, text="New", command=self.new_click)
        self.new_button.grid(column=0, row=0, columnspan=2)
        self.exit_button = tk.Button(self.window, text="Exit", command=self.exit_click)
        self.exit_button.grid(column=2, row=0, columnspan=2)
        self.numbers = tuple((tk.Button(self.window, text=str(i + 1), command=self.number_click(i)) for i in range(15)))
        self.new_click()

    def new_click(self):
        self.buttons_positions = list(range(15))
        random.shuffle(self.buttons_positions)
        while not self.check_combination(self.buttons_positions):
            random.shuffle(self.buttons_positions)
        # пустота
        self.buttons_positions.append(None)
        self.grid()

    def exit_click(self):
        self.window.destroy()

    def grid(self):
        for i, button_id in enumerate(self.buttons_positions):
            if button_id is None:
                continue
            self.numbers[button_id].grid(column=i % 4, row=1 + i // 4, sticky=tk.NSEW)

    def number_click(self, n):
        def move():
            n_pos = self.buttons_positions.index(n)
            n_y, n_x = divmod(n_pos, 4)
            none_coord = self.buttons_positions.index(None)
            none_y, none_x = divmod(none_coord, 4)
            if n_x == none_x and abs(n_y-none_y) == 1 or abs(n_x - none_x) == 1 and n_y == none_y:
                self.buttons_positions[n_pos], self.buttons_positions[none_coord] = \
                    self.buttons_positions[none_coord], self.buttons_positions[n_pos]
            self.grid()
            if self.won():
                tk.messagebox.showinfo(message="Won!")
                self.new_click()
        return move

    def check_combination(self, order):
        """
        поверка комбинации на собираемость (взято с википедии), е = 4 - четное, поэтому исключаем из суммы
        :param order:
        :return:
        """
        N = 0
        for i_idx, i in enumerate(order):
            for j in range(i_idx + 1, 15):
                N += int(i > order[j])

        return N % 2 == 0

    def won(self):
        won = True
        for idx, n in enumerate(self.buttons_positions[:-1]):
            if idx != n:
                won = False
        return won

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    random.seed(42)
    game = Game15()
    game.run()