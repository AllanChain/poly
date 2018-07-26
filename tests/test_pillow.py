from PIL import Image, ImageDraw,ImageFont
from poly import poly,PolyGroup
from math import pi

#pd=[]
a=poly(n=6,r=40,topleft=(60,260),lie=True,rotate_rad=pi/2)
#pd.append(a)
#pd.append(poly(n=6,r=40,topleft=(0,a.rect[1]),lie=True))

ps=PolyGroup(EVEN=3,ODD=3,line=5,base_poly=a,SINK=True)#,rotate_rad=0.1)
print(ps.get_neibors_by_num(6))
im = Image.new("RGBA",(500,500),(0,0,0))

font=ImageFont.load_default()
draw = ImageDraw.Draw(im)
j=0
for a in ps:
    #print(a.points)
    draw.polygon(a.points,outline=(0,255,0),fill=(0,0,255))
    k=ps.coord_to_num(ps.num_to_coord(j))
    draw.text(a.center,str(j),font=font)
    j+=1
    #for i in range(len(a.points)):
        #draw.text(a.points[i],str(i),font=font)
        #print(i)
#x0,y0,dx,dy=ps.rect
#draw.rectangle([x0,y0,x0+dx,y0+dy])
draw.rectangle(ps.rect.ixyxy)
im.save('test_img.png', "PNG")
