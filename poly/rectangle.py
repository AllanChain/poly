DELTA={'topleft':(0,0),
       'topright':(1,0),
       'center':(0.5,0.5),
       'bottomleft':(0,1),
       'bottomright':(1,1)}
class Rect:
    __slots__=('x0','y0','w','h')
    def __init__(self,rect):
        self.x0,self.y0,self.w,self.h=rect
    def collide(self,p):
        x,y=p
        if self.x0<=x<=self.x0+self.w and self.y0<=y<=self.y0+self.h:
            return True
        return False
    def __getattr__(self,attr):
        to_int=False
        response=[]
        if attr.startswith('i'):
            to_int=True
            attr=attr[1:]
        if attr=='xyxy':
            response=(self.x0,self.y0,self.x0+self.w,self.y0+self.h)
        else:
            if 'xy' in attr:
                response.extend([self.x0,self.y0])
            if 'wh' in attr:
                response.extend([self.w,self.h])
        if attr in DELTA:
            response=(self.x0+self.w*DELTA[attr][0],\
                      self.y0+self.h*DELTA[attr][1])
        if to_int==True:
            response=list(map(int,response))
        return tuple(response)
    def move(self,d):
        self.x0+=d[0]
        self.y0+=d[1]
    def __str__(self):
        #print('here')
        return f'Rect<Topleft:{self.itopleft} Wh:{self.iwh}>'
##    @property
##    def xywh(self):
##        return self.x0,self.y0,self.w,self.h
##    @property
##    def topleft(self):
##        return self.x0,self.y0
##    @property
##    def wh(self):
##        return self.w,self.h
##    @property
##    def iwh(self):
##        return int(self.w),int(self.h)
##    @property
##    def center(self):
##        return self.x0+self.w/2,self.y0+self.h/2
##    @property
##    def icenter(self):
##        return int(self.x0+self.w/2),int(self.y0+self.h/2)
##
