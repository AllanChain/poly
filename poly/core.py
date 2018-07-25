from math import sin,cos,pi
from . import rectangle
from copy import deepcopy

def getline(p1,p2):
    x1,y1=p1
    x2,y2=p2
    if abs(y1-y2)>100*abs(x1-x2):
        return(None,None)
    k=(y1-y2)/(x1-x2)
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
    def move(self,d):
        dx,dy=d
        add=lambda p:(p[0]+dx,p[1]+dy)
        self.points=list(map(add,self.points))
    def copy_and_move(self,d):
        polyobj=deepcopy(self)
        polyobj.move(d)
        return polyobj
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
    sang=pi/n if lie else 0#start angle
    step=pi*2/n
    points=[]
    for i in range(n):
        ang=i*step+sang
        points.append((sin(ang)*r,cos(ang)*r))#由下方或偏右逆时针编号
    self=commonPoly(points)
    self.r,self.size=r,size
    self.regular=True
    if center!=None:
        sx,sy=center
        self.move(center)
        self.center=(sx,sy)
        self.rect.move(center)
    else:
        dx=topleft[0]-self.topleft[0]
        dy=topleft[1]-self.topleft[1]
        self.move((dx,dy))
        self.rect.move((dx,dy))
        self.center=(dx,dy)
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
