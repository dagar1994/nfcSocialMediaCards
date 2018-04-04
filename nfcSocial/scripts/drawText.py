from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("Copilme-Regular.ttf", 25)
size = font.getsize("Hello World")
img = Image.new('RGB', size )
d = ImageDraw.Draw(img)
d.text((0,0), "Hello World", fill=("#ffdc7d"),font = font)

img.save('pil_text.png')
