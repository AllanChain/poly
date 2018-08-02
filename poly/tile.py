# handling tiling hexagons and octagons
from . import poly,Rect
from math import sin,cos


class PolyError(Exception):
    pass
class PolyGroup:
    def __init__(self,EVEN,ODD,line,base_poly,SINK=True):
        if EVEN<1 or ODD<1 or line<1:
            raise PolyError('Cannot create such a poly: negtive settings.')
        self.r_poly=base_poly
        if base_poly.rotate_rad!=0:
            base_poly=base_poly.copy_and_rotate(-base_poly.rotate_rad)
            print(base_poly.rect)
            print(self.r_poly.rect)
            print(base_poly.ipoints)
        self.n=base_poly.n
        if not self.n in (6,8):
            raise PolyError('Cannot create such a poly: not implemented')
        self.__dict__.update(locals())
        del self.__dict__['self']
        self.ODD_T=ODD
        self.EVEN_T=EVEN
        if abs(EVEN-ODD)==1:
            pass
        elif EVEN==ODD:
            if SINK:#首行下沉
                self.ODD+=1
            else:
                self.EVEN+=1
        else:
            raise PolyError('Cannot create such a poly group')
        f=(self.EVEN-self.ODD-2*self.EVEN_T+2*self.ODD_T)
        if self.n==6:
            self.dlx=base_poly.points[0][0]-base_poly.points[4][0]
            self.dly=base_poly.rect.h
            print(self.dlx)
            down=max(0,f)*self.dly/2+self.dly
        elif self.n==8:
            self.dlx=base_poly.points[0][0]-base_poly.points[5][0]
            self.dly=base_poly.size+base_poly.rect.h
            down=max(base_poly.size+base_poly.rect.h,f*(base_poly.points[0][1]-base_poly.points[1][1]+self.dly))
        up=min(0,(self.EVEN-self.ODD)/2)*self.dly
        #print(down)
        self.rect=Rect((self.base_poly.topleft[0],self.base_poly.topleft[1]+up,\
                   self.dlx*line+base_poly.points[1][0]-base_poly.points[0][0],\
                   self.dly*(self.EVEN_T-1)+down-up))
        r,s=divmod(line,2)
        self.total=r*(self.EVEN_T+self.ODD_T)+s*self.EVEN_T
        self.rotate_sin=sin(self.r_poly.rotate_rad)
        print(self.r_poly.rotate_rad)
        self.rotate_cos=cos(self.r_poly.rotate_rad)
        return
    def __getitem__(self,i):
        coord=self.num_to_coord(i)
        self.check_valid_coord(coord)
        return self.get_poly_by_coord(coord)

    def get_delta_pos_by_coord(self,coord):
        self.check_valid_coord(coord)
        x,y=coord
        dx=x*self.dlx
        dy=self.dly*(y+(x%2)*(self.EVEN-self.ODD)/2)
        #return dx,dy
        return dx*self.rotate_cos+dy*self.rotate_sin,-dx*self.rotate_sin+dy*self.rotate_cos
    def get_pos_by_coord(self,coord):
        sx,sy=self.base_poly.topleft
        dx,dy=self.get_delta_pos_by_coord(coord)
        return sx+dx,sy+dy
    def get_poly_by_coord(self,coord):
        dx,dy=self.get_delta_pos_by_coord(coord)
        poly_obj=self.r_poly.copy_and_move((dx,dy))
        return poly_obj
    def is_valid_coord(self,coord):
        x,y=coord
        if x<0 or y<0:
            return False
        if x>=self.line:
            return False
        if x%2==1 and y>=self.ODD:
            return False
        if x%2==0 and y>=self.EVEN:
            return False
        return True
    def collide(self,pos):
        if not self.rect.collide(pos):
            return False
        sx,sy=pos
        cx,cy=self.base_poly.topleft
        sx-=cx
        sy-=cy
        sx=sx*self.rotate_cos-sy*self.rotate_sin
        sy=sy*self.rotate_cos+sx*self.rotate_sin
        x=int(sx//self.dlx)
        y=int(sy//self.dly)
        ns=self.get_neiborhood_by_coord((x,y))
        for p in ns:
            t_poly=self.get_poly_by_coord(p)
            print('---'*3)
            if t_poly.collide(pos):
                return p
    def check_valid_coord(self,coord):
        if not self.is_valid_coord(coord):
            raise IndexError('Index out of range')
        else:
            return
    def num_to_coord(self,num):
        EVEN,ODD=self.EVEN_T,self.ODD_T
        p,q=divmod(num,(EVEN+ODD))
        #r,s=divmod(q,self.EVEN)
        r=min(1,q//EVEN)#r可能为2
        x,y=p*2+r,q-r*EVEN
        self.check_valid_coord((x,y))
        return x,y
    def coord_to_num(self,coord):
        self.check_valid_coord(coord)
        x,y=coord
        EVEN,ODD=self.EVEN_T,self.ODD_T
        return (x//2)*(EVEN+ODD)+(x%2)*EVEN+y
    def get_neibors_by_coord(self,coord):
        #self.check_valid_coord(coord)
        x,y=coord
        neibors=[(x+1,y),(x-1,y),(x+1,y+((x%2)*2-1)*(self.EVEN-self.ODD)),\
                 (x-1,y+((x%2)*2-1)*(self.EVEN-self.ODD))]
        if self.n==6:
            neibors.extend([(x,y+1),(x,y-1)])
        neibors=list(filter(self.is_valid_coord,neibors))
        
        return neibors
    def get_neiborhood_by_coord(self,coord):
        x,y=coord
        neiborhood=[(x,y),(x+1,y),(x-1,y),(x,y+1),(x,y-1),\
                (x+1,y+((x%2)*2-1)*(self.EVEN-self.ODD)),\
                (x-1,y+((x%2)*2-1)*(self.EVEN-self.ODD)),]
        neiborhood=list(filter(self.is_valid_coord,neiborhood))
        return neiborhood

    def get_neibors_by_num(self,num):
        coord=self.num_to_coord(num)
        return(list(map(self.coord_to_num,self.get_neibors_by_coord(coord))))
class ComboGroup:
    def __init__(self,groups):
        self.groups=groups
        self.totals=[g.total for g in groups]
        self.total=sum(self.totals)
        self.group_number=len(groups)

    def __getitem__(self,*args):
        if len(args)==1:
            g,n=self.get_group(args[0])
            if g==None:
                raise IndexError('Index out of range')
            return g[n]
        elif len(args)==3:
            return self.groups[args[0]].get_poly_by_coord(arg[1:])

    def get_group(self,n):
        if 0<=n<self.total:
            for g in self.groups:
                if n<g.total:
                    return g,n
                n-=g.total
        return(None,None)
    def collide(self,p):
        for i in range(len(self.groups)):
            po=self.groups[i].collide(p)
            if po:
                return (i,)+po
        return None
    def coord_to_num(self,coord):
        n=0
        for i in range(coord[0]):
            n+=self.totals[i]
        n+=self.groups[coord[0]].coord_to_num(coord[1:])
        return n
    def num_to_coord(self,num):
        if 0<=num<self.total:
            for i in range(self.group_number):
                if num<self.totals[i]:
                    return (i,)+self.groups[i].num_to_coord(num)
                num-=self.totals[i]
        return(None,None)
    def get_pos_by_num(self,num):
        g,n=self.get_group(num)
        coord=g.num_to_coord(n)
        return g.get_pos_by_coord(coord)
    def set_special_neibors(self,sdict,mutual=True):
        self.specials={}
        for k,v in sdict.items():
            print(self.specials,k,v)
            self.specials[k]=set(v)
            if mutual==True:
                for j in v:
                    if j in self.specials:
                        self.specials[j].add(k)
                    else:
                        self.specials[j]=set((k,))
    def get_neibors_by_num(self,num):
        neibors=[]
        total=sum(self.totals[:self.num_to_coord(num)[0]])
        if hasattr(self,'specials'):
            neibors+=list(self.specials.get(num,[]))
        g,n=self.get_group(num)
        neibors+=map(lambda x:x+total,g.get_neibors_by_num(n))
        return neibors
    # def get_neibors_by_coord(self,coord):
    #     neibors=[]
    #     neibors+=self.groups[coord[0]].get_neibors_by_coord(coord[1:])
    #
