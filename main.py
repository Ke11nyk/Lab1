from tkinter import *
from tkinter import ttk
import time

class Game:
    def __init__(self):
        self.__tk = Tk()
        self.__tk.title("Game")
        self.__tk.resizable(0, 0)
        self.__tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.__tk, width=500, height=500, highlightthickness=0)
        self.canvas.pack()
        self.__tk.update()
        self.canvas_height = 500
        self.canvas_width = 500
        self.__bg = PhotoImage(file="background.gif")
        w = self.__bg.width()
        h = self.__bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x * w, y * h, image=self.__bg, anchor='nw')
        self.sprites = []
        self.running = True
        self.__game_over_text = self.canvas.create_text(250, 250, text='YOU WON!', state='hidden')
        self.__last_time = time.time()
        self.label = ttk.Label(self.__tk, text=f"Time: {int(time.time() - self.__last_time)} seconds")
        self.label.pack(side=RIGHT)

    def get_tk(self):
        return self.__tk

    def mainloop(self):
        while 1:
            if self.running == True:
                self.label["text"] = f"Time: {int(time.time() - self.__last_time)} seconds"
                for sprite in self.sprites:
                    sprite.move()
            else:
                time.sleep(1)
                self.canvas.itemconfig(self.__game_over_text, state='normal')
            self.__tk.update_idletasks()
            self.__tk.update()
            time.sleep(0.01)

class Button:
    def __init__(self, game, tk, text):
        self.game = game
        self.tk = tk
        self.clicks = 0
        self.text = text
        self.btn = ttk.Button(self.tk, text=self.text, command=self.click_button)
        self.btn.pack(side=LEFT)

    def click_button(self):
        pass

class RestartButton(Button):
    def __init__(self, game, tk, text):
        Button.__init__(self, game, tk, text)

    def click_button(self):
        self.tk.destroy()
        main()

class ExitButton(Button):
    def __init__(self, game, tk, text):
        Button.__init__(self, game, tk, text)

    def click_button(self):
        self.tk.destroy()

class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None
    def move(self):
        pass
    def coords(self):
        return self.coordinates

class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.__photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.__photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)

class MovingPlatformSprite(PlatformSprite):
    def __init__(self, game, photo_image, x, y, width, height):
        PlatformSprite.__init__(self, game, photo_image, x, y, width, height)
        self.x = 2
        self.counter = 0
        self.__last_time = time.time()
        self.width = width
        self.height = height

    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + self.width
        self.coordinates.y2 = xy[1] + self.height
        return self.coordinates

    def move(self):
        if time.time() - self.__last_time > 0.03:
            self.__last_time = time.time()
            self.game.canvas.move(self.image, self.x, 0)
            self.counter = self.counter + 1
            if self.counter > 20:
                self.x = self.x * -1
                self.counter = 0

class StickFigureSprite(Sprite):
    def __init__(self, game, tk):
        Sprite.__init__(self, game)
        self.__images_left = [
            PhotoImage(file="figure-L1.gif"),
            PhotoImage(file="figure-L2.gif"),
            PhotoImage(file="figure-L3.gif")
        ]
        self.__images_right = [
            PhotoImage(file="figure-R1.gif"),
            PhotoImage(file="figure-R2.gif"),
            PhotoImage(file="figure-R3.gif")
        ]
        self.image = game.canvas.create_image(200, 470, image=self.__images_left[0], anchor='nw')
        self.x = -2
        self.y = 0
        self.__current_image = 0
        self.__current_image_add = 1
        self.__jump_count = 0
        self.__last_time = time.time()
        self.coordinates = Coords()
        self.tk = tk
        self.__count = 0
        self.label = ttk.Label(self.tk, text=f"")
        self.label.pack(side=RIGHT)
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<KeyPress-Up>', self.jump)

    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2

    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2

    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.__jump_count = 0
        self.__count += 1
        self.label["text"] = f"You made {self.__count} jump" if self.__count == 1 else f"You made {self.__count} jumps"

    def get_count(self):
        return self.__count

    def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.__last_time > 0.1:
                self.__last_time = time.time()
                self.__current_image += self.__current_image_add
                if self.__current_image >= 2:
                    self.__current_image_add = -1
                if self.__current_image <= 0:
                    self.__current_image_add = 1
        __images_to_use = self.__images_left if self.x < 0 else self.__images_right
        if self.y != 0:
            self.game.canvas.itemconfig(self.image, image=__images_to_use[2])
        else:
            self.game.canvas.itemconfig(self.image, image=__images_to_use[self.__current_image])

    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates

    def within_x(self, co1, co2):
        if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
                or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
                or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
                or (co2.x2 > co1.x1 and co2.x2 < co1.x2):
            return True
        else:
            return False

    def within_y(self, co1, co2):
        if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
                or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
                or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
                or (co2.y2 > co1.y1 and co2.y2 < co1.y2):
            return True
        else:
            return False

    def collided_left(self, co1, co2):
        if self.within_y(co1, co2):
            if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
                return True
        return False

    def collided_right(self, co1, co2):
        if self.within_y(co1, co2):
            if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
                return True
        return False

    def collided_top(self, co1, co2):
        if self.within_x(co1, co2):
            if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
                return True
        return False

    def collided_bottom(self, y, co1, co2):
        if self.within_x(co1, co2):
            y_calc = co1.y2 + y
            if y_calc >= co2.y1 and y_calc <= co2.y2:
                return True
        return False

    def move(self):
        self.animate()
        if self.y < 0:
            self.__jump_count += 1
            if self.__jump_count > 20:
                self.y = 4
        if self.y > 0:
            self.__jump_count -= 1
        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False
        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y < 0 and self.collided_top(co, sprite_co):
                self.y = -self.y
                top = False
            if bottom and self.y > 0 and self.collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False
            if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height and self.collided_bottom(1, co, sprite_co):
                falling = False
            if left and self.x < 0 and self.collided_left(co, sprite_co):
                self.x = 0
                left = False
                if sprite.endgame:
                    self.end(sprite)
            if right and self.x > 0 and self.collided_right(co, sprite_co):
                self.x = 0
                right = False
        if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
            self.y = 4
        self.game.canvas.move(self.image, self.x, self.y)

    def end(self, sprite):
        self.game.running = False
        sprite.opendoor()
        time.sleep(1)
        self.game.canvas.itemconfig(self.image, state='hidden')
        sprite.closedoor()

class DoorSprite(Sprite):
    def __init__(self, game, x, y, width, height):
        Sprite.__init__(self, game)
        self.__closed_door = PhotoImage(file="door1.gif")
        self.__open_door = PhotoImage(file="door2.gif")
        self.__image = game.canvas.create_image(x, y, image=self.__closed_door, anchor='nw')
        self.coordinates = Coords(x, y, x + (width / 2), y + height)
        self.endgame = True
        self.tk = game.get_tk()

    def opendoor(self):
        self.game.canvas.itemconfig(self.__image, image=self.__open_door)
        self.tk.update_idletasks()

    def closedoor(self):
        self.game.canvas.itemconfig(self.__image, image=self.__closed_door)
        self.tk.update_idletasks()

def main():
    g = Game()

    platform1 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 0, 480, 100, 10)
    platform2 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 150, 440, 100, 10)
    platform3 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 300, 400, 100, 10)
    platform4 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 300, 160, 100, 10)
    platform5 = MovingPlatformSprite(g, PhotoImage(file="platform2.gif"), 175, 350, 66, 10)
    platform6 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 50, 300, 66, 10)
    platform7 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 170, 120, 66, 10)
    platform8 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 45, 60, 66, 10)
    platform9 = MovingPlatformSprite(g, PhotoImage(file="platform3.gif"), 170, 250, 32, 10)
    platform10 = PlatformSprite(g, PhotoImage(file="platform3.gif"), 230, 200, 32, 10)

    g.sprites.append(platform1)
    g.sprites.append(platform2)
    g.sprites.append(platform3)
    g.sprites.append(platform4)
    g.sprites.append(platform5)
    g.sprites.append(platform6)
    g.sprites.append(platform7)
    g.sprites.append(platform8)
    g.sprites.append(platform9)
    g.sprites.append(platform10)

    door = DoorSprite(g, 45, 30, 40, 35)
    g.sprites.append(door)

    sf = StickFigureSprite(g, g.get_tk())
    g.sprites.append(sf)

    restart = RestartButton(g, g.get_tk(), "Restart")
    exit = ExitButton(g, g.get_tk(), "Exit")

    g.mainloop()

main()