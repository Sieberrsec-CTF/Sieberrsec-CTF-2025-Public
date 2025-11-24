from PIL import Image

img = Image.open("/absolute/path/to/i_hate_guessy_stego_1.png") # REPLACE WITH ACTUAL PATH

pixels = list(img.getdata())

data = []
for pixel in pixels:
    data += [*pixel]

data = bytes(data)
data = data.decode('utf-16le')

print(data[:data.index("}")+1]) # the flag was repeated 95000 times