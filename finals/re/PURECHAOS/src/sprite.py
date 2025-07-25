from PIL import Image, ImageTk

from gui import *

class Sprite:
    def __init__(self, image_src, x, y, width, height):
        self.image = ImageTk.PhotoImage(Image.open(image_src).resize((width, height)))
        
        self.object = canvas.create_image(x, y, image=self.image, anchor=tk.NW)
    
    def shift(self, x, y):
        canvas.move(self.object, x, y)

    def get_bounds(self):
        box = canvas.bbox(self.object)

        width, height = box[2] - box[0], box[3] - box[1]

        return (*box[:2], width, height)
    
    def destroy(self):
        self.image.__del__()