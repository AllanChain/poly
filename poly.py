from math import sin,cos,pi

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
    def collide(self,p):
        x,y=p
        linein=[]
        if not (self.topleft[0]<=x<=self.topleft[0]+self.rect[0] and \
               self.topleft[1]<=y<=self.topleft[1]+self.rect[1]):#in the rect
           return False
        flag=1 if self.points[-1][0]<=x else -1
        for i in range(-1,self.n-1):
           x0=self.points[i+1][0]
           '''if x0<x:
              flag2=1
           elif x0==x:
              flag2=flag
           else:
              flag2=-1'''
           flag2=1 if x0<x else -1
           if flag!=flag2:
              flag=flag2
              k,b=getline(self.points[i+1],self.points[i])
              if k!=None:
                  linein.append(k*x+b)
    
        linein.sort()
        #print(linein)
        bools=list(map(lambda y0:y>=y0,linein))
        num=bools.count(True)
        ans=True if num%2==1 else False
        return ans
class poly(commonPoly):
    def __init__(self,n,r=None,size=None,topleft=(0,0),center=None,lie=True):
        '''def __init__(self,n,r=None,size=None,topleft=(0,0),lie=True)
n is the num of size of the poly;
'''
        assert n<=20,'n is too large'
        assert n>=3,'n is too small'
        assert int(n)==n,'n must be an integer'
        assert isinstance(r, (int, float)) or isinstance(size, (int, float)),\
              'The r or size must be an number'
        if size!=None and r==None:
            r=(size/2)/sin(pi/n)
        
            #topleft=(size/2)/sin(pi/n)
        if n % 2==0:#if it's an even one
            if n%4==2:
                rect=(r*2,r*2*cos(pi/n)) if lie else (r*2*cos(pi/n),r*2)
                    #the rect that holds the poly
            else:
                rect=(r*2*cos(pi/n),r*2*cos(pi/n))
            sx,sy=rect[0]/2,rect[1]/2
        else:#an odd one
            rect=(r*sin((n//2)*pi/n)*2,r*cos(pi/n)+r)
            sx=r*sin((n//2)*pi/n)
            sy=r if lie else r*cos(pi/n)
        if center!=None:
            topleft=(center[0]-rect[0]/2,center[1]-rect[1]/2)
            #print(rect)
        x,y=topleft
        sx+=x
        sy+=y
        sang=pi/n if lie else 0#start angle
        step=pi*2/n
        points=[]
        for i in range(n):
            ang=i*step+sang
            points.append((int(sx+sin(ang)*r),int(sy+cos(ang)*r)))
        self.rect,self.topleft,self.points=rect,topleft,points
        self.n,self.r,self.size=n,r,size
        #print(sx)
    def __str__(self):
        return 'A poly with %d edge and %d r'%(self.n,self.r)
   
       
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
                    DIS.fill((0,0,0))
                    pygame.draw.polygon(DIS,(255,0,0),t.points,5)
                    pygame.display.update()
                    print(t)
if __name__=='__main__':
    import pygame
    from pygame.locals import *
    from random import randint
    main()
