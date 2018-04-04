from PIL import Image
img = Image.open('qr.png', 'r').convert("RGBA")
img2 = Image.open('pil_text.png', 'r').convert("RGBA")
img2 = img2.rotate(90, expand=1)
img_w, img_h = img.size
img_w2, img_h2 = img2.size
background = Image.open('kk.png')
bg_w, bg_h = background.size
offset = (((bg_w - img_w) // 2) -50 , (bg_h - img_h) // 2)
offset2 = (((bg_w - img_w2) // 2) +100 , ((bg_h - img_h2) // 2) )
background.paste(img, offset,mask=img)
background.paste(img2, offset2,mask=img2)
background.save('out.png', format="png")
