from PIL import Image, ImageDraw,ImageFont
from poly import poly,PolyGroup

a=poly(n=6,r=40,topleft=(0,0),lie=True)#False,start_rad=0.2)
X,Y=POINT=30,40
print(a.collide(POINT))
im = Image.new("RGBA",(100,100),(0,0,0))
font=ImageFont.load_default()
draw = ImageDraw.Draw(im)
j=0
draw.polygon(a.points,outline=(0,255,0),fill=(0,0,255))
for p in a.ipoints:
    print(p)
    draw.text(p,str(j),font=font)
    j+=1
draw.ellipse((X-5,Y-5,X+5,Y+5),fill=(0,255,0))
draw.rectangle(a.rect.ixyxy)
im.save('test_img2.png', "PNG")
