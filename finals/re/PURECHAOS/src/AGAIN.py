import sys
sys.dont_write_bytecode = True

import random

from sprite import *
import eggsor

speed = 5
ticks = 0
score = 0

player = Sprite("assets/player.png", screen_width / 2 - 40, screen_width - 100, 80, 100)
legos = []

score_text = canvas.create_text(0, 0, text="", anchor='nw', font=("Arial", 16), fill="white")

def spawn_lego():
    width = 100
    
    lego = Sprite("assets/lego.png", random.randint(0, screen_width - width), 0, width, 50)
    legos.append(lego)

def gameloop():
    global ticks, score
    
    canvas.itemconfig(score_text, text=f"Score: {score}")
    
    if ticks % 50 == 0:
        ticks = 0
        spawn_lego()

    for lego in legos[::-1]:
        player_bounds = player.get_bounds()
        lego_bounds = lego.get_bounds()

        if not (player_bounds[0] + player_bounds[2] < lego_bounds[0] or player_bounds[0] > lego_bounds[0] + lego_bounds[2] or player_bounds[1] + player_bounds[3] < lego_bounds[1] or player_bounds[1] > lego_bounds[1] + lego_bounds[3]):
            lego.destroy()
            legos.remove(lego)
            score += 1

        elif lego_bounds[1] > screen_width:
            lego.destroy()
            legos.remove(lego)
            
        lego.shift(0, speed)

    if keys["A"]:
        if player.get_bounds()[0] > 0:
            player.shift(-speed, 0)
    if keys["D"]:
        if player.get_bounds()[0] + player.get_bounds()[2] < screen_width:
            player.shift(speed, 0)

    ticks += 1
    root.after(10, gameloop)

gameloop()
root.mainloop()

player.destroy()
for lego in legos:
    lego.destroy()