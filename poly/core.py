from math import sin,cos,pi
from . import rectangle

def getline(p1,p2):
    x1,y1=p1
    x2,y2=p2
    if  x1==x2:
        return(None,None)
    k=(y1-y2)/(x1-x2)
    if k>100:return(None,None)
    b=y1-k*x1
    return(k,b)


class commonPoly:
    def __init__(self,points):
        self.points=points
        self.n=len(points)
        self.set_data()
    def set_data(self):
        xs=[x for x,y in self.points]
        ys=[y for x,y in self.points]
        x0=min(xs)
        x1=max(xs)
        y0=min(ys)
        y1=max(ys)
        self.rect=rectangle.Rect((x0,y0,x1-x0,y1-y0))
        self.topleft=(x0,y0)
    def collide(self,p):
        if hasattr(self,'rect'):
            if not self.rect.collide(p):
                return False
        x,y=p
        linein=[]
        flag=1 if self.points[-1][0]<=x else -1
        for i in range(-1,self.n-1):
           x0=self.points[i+1][0]
           flag2=1 if x0<x else -1
           if flag!=flag2:
              flag=flag2
              k,b=getline(self.points[i+1],self.points[i])
              if k!=None:
                  linein.append(k*x+b)
        linein.sort()
        bools=list(map(lambda y0:y>=y0,linein))
        num=bools.count(True)
        ans=True if num%2==1 else False
        return ans
    def copy_and_move(self,d):
        dx,dy=d
        #ox,oy=self.topleft
        points=self.points.copy()
        add=lambda p:(p[0]+dx,p[1]+dy)
        polyobj=commonPoly(list(map(add,points)))
        #polyobj.topleft=(self.topleft[0]+dx,self.topleft[1]+dy)
        #polyobj.rect=rectangle.Rect(polyobj.topleft+self.rect.wh)
        polyobj.n,polyobj.r,polyobj.size=self.n,self.r,self.size
        polyobj.center=(self.center[0]+dx,self.center[1]+dy)
        return polyobj
        #return poly(n=self.n,r=self.r,topleft=(ox+dx,oy+dy))
    def __str__(self):
        return 'A poly with %d edge and %d r'%(self.n,self.r)

def poly(n,r=None,size=None,topleft=(0,0),center=None,lie=True):
    assert n<=20,'n is too large'
    assert n>=3,'n is too small'
    assert int(n)==n,'n must be an integer'
    assert isinstance(r, (int, float)) or isinstance(size, (int, float)),\
          'The r or size must be an number'
    if size!=None and r==None:
        r=(size/2)/sin(pi/n)
    else:
        size=r*sin(pi/n)*2
        #topleft=(size/2)/sin(pi/n)
    if n % 2==0:#if it's an even one
        if n%4==2:
            rect=(r*2,r*2*cos(pi/n)) if lie else (r*2*cos(pi/n),r*2)
                #the rect that holds the poly
        else:
            rect=(r*2*cos(pi/n),r*2*cos(pi/n)) if lie else (r*2,r*2)
        sx,sy=rect[0]/2,rect[1]/2
    else:#an odd one
        rect=(r*sin((n//2)*pi/n)*2,r*cos(pi/n)+r)
        sx=r*sin((n//2)*pi/n)
        sy=r if lie else r*cos(pi/n)
    if center!=None:
        topleft=(center[0]-rect[0]/2,center[1]-rect[1]/2)
        #以center为准，可能和圆心不重合！！
    x,y=topleft
    sx+=x
    sy+=y
    sang=pi/n if lie else 0#start angle
    step=pi*2/n
    points=[]
    for i in range(n):
        ang=i*step+sang
        points.append((int(sx+sin(ang)*r),int(sy+cos(ang)*r)))#由下方或偏右逆时针编号
    self=commonPoly(points)
    self.topleft=topleft
    self.rect=rectangle.Rect(topleft+rect)
    self.n,self.r,self.size=n,r,size
    self.center=(sx,sy)
    #print(sx)
    return self
   
       
def main():
    pygame.init()
    DIS=pygame.display.set_mode((400,400))
    t=poly(n=8,size=40)
    print(t.rect,t.r)
    pygame.draw.polygon(DIS,(255,0,0),t.points,5)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                return
            if event.type==MOUSEBUTTONDOWN:
                if t.collide(event.pos):
                    print('In')
                    #print(t)
                else:
                    print('Out')
            elif event.type==KEYDOWN:
                #print(event.key)
                if event.key== 13:
                    t=poly(n=randint(3,15),r=150)
                    print(t.rect.itopleft)
                    DIS.fill((0,0,0))
                    pygame.draw.polygon(DIS,(255,0,0),t.points,5)
                    pygame.display.update()
                    print(t)
if __name__=='__main__':
    import pygame
    from pygame.locals import *
    from random import randint
    main()
