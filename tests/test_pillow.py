from PIL import Image, ImageDraw,ImageFont
from poly import poly,PolyGroup
from math import pi

a=poly(n=6,r=40,topleft=(0,0),lie=True)#,rotate_rad=pi/2)
X,Y=POINT=((80,70))
ps=PolyGroup(EVEN=3,ODD=3,line=5,base_poly=a,SINK=True)#,rotate_rad=0.1)
print('co@@',ps.collide(POINT))
print(ps.get_neibors_by_num(6))
im = Image.new("RGBA",(700,700),(0,0,0))

font=ImageFont.load_default()
draw = ImageDraw.Draw(im)
j=0
for a in ps:
    #print(a.points)
    draw.polygon(a.points,outline=(0,255,0),fill=(0,0,255))
    k=ps.coord_to_num(ps.num_to_coord(j))
    draw.text(a.rect.center,str(j),font=font)
    draw.rectangle(a.rect.xyxy)
    j+=1
draw.ellipse((X-5,Y-5,X+5,Y+5),fill=(0,255,0))
draw.rectangle(ps.rect.ixyxy)
im.save('test_img.png', "PNG")
