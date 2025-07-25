import tkinter as tk
import string

screen_width = 600

keys = {i: False for i in [c for c in string.ascii_uppercase + string.digits] + ["SPACE", "ENTER"]}

def update_key(e, switch):
    key = [e.keysym, "enter"][e.keysym.lower() == "return"].upper()
    keys[key] = switch

root = tk.Tk()
root.wm_title("let's do some legos")
root.resizable(0,0)
root.protocol("WM_DELETE_WINDOW", root.destroy)

root.bind("<KeyPress>", lambda e: update_key(e, 1))
root.bind("<KeyRelease>", lambda e: update_key(e, 0))

canvas = tk.Canvas(root, width=screen_width, height=screen_width, bg="black", borderwidth=0, highlightthickness=0)
canvas.pack()