import tkinter as tk
import settings
import values
import utils
from random import randint


def tksleep(self, time: float) -> None:
    """
    Emulating `time.sleep(seconds)`
    Created by TheLizzard, inspired by Thingamabobs
    """
    self.after(int(time*1000), self.quit)
    self.mainloop()
tk.Misc.tksleep = tksleep


def game_setup(window):
    window.configure(bg="black")
    window.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
    window.title("Click Game")
    window.resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", on_closing)


def on_closing():
    quit()


def game_reset(event):
    highscore_label.config(text=f'Highscore: {highscore}')

    values.score = 0
    score_label.config(text=values.score)
    values.game_over = False
    reset_button.place_forget()


class Cell:
    def __init__(self):
        self.cell_button_object = None
        self.is_visible = False

    def create_button_object(self, location):
        btn = tk.Button(location)
        btn.bind('<Button-1>', self.left_click_action)
        self.cell_button_object = btn
        root.after(1000, self.destroy_button)  # this was problematic when in cell.py

    def left_click_action(self, event):  # this uses variables form outside the scope
        values.score += 1
        score_label.config(text=values.score)
        self.cell_button_object.destroy()
        self.is_visible = False

    def destroy_button(self):
        if self.is_visible is True:
            self.cell_button_object.destroy()
            values.game_over = True


root = tk.Tk()
game_setup(root)


top_frame = tk.Frame(
    root,
    bg='black',
    width=settings.WIDTH,
    height=utils.height_prct(10)
)
top_frame.place(x=0, y=0)

center_frame = tk.Frame(
    root,
    bg='black',
    width=settings.WIDTH,
    height=utils.height_prct(90)
)
center_frame.place(x=0, y=utils.height_prct(10))


score_label = tk.Label(
    text='0',
    foreground='white',
    background='black'
)
score_label.config(font=("Courier", 25))
score_label.place(x=0, y=0, width=50, height=40)

file = open('highscore.txt')
highscore = int(file.readline())
file.close()

highscore_label = tk.Label(
    text=f'Highscore: {highscore}',
    foreground='white',
    background='black'
)
highscore_label.config(font=("Courier", 10))
highscore_label.place(x=280, y=0, width=120, height=40)


reset_button = tk.Button(center_frame, text='GAME OVER\n\nClick to play again.', foreground='white', background='black')
reset_button.config(font=("Courier", 20))
reset_button.bind('<Button-1>', game_reset)


while True:
    if values.game_over is False:
        c = Cell()
        c.create_button_object(center_frame)
        random_x = randint(0, (settings.WIDTH - settings.EDGE_SIZE))
        random_y = randint(utils.height_prct(10), 335)  # 335 figured out by trial and error, didn't work with -EDGE_SIZE
        c.cell_button_object.place(x=random_x, y=random_y, width=settings.EDGE_SIZE, height=settings.EDGE_SIZE)
        c.is_visible = True
        root.tksleep(0.6)
    if values.game_over is True:
        reset_button.place(x=-5, y=-5, width=410, height=370)
        c.destroy_button()
        if values.score > highscore:
            highscore = values.score
            file = open("highscore.txt", "w")
            file.write(str(highscore))
            file.close()
        root.tksleep(0.1)
