# handling tiling hexagons and octagons
from . import poly
class PolyError(Exception):
    pass
class PolyGroup:
    def __init__(self,EVEN,ODD,line,base_poly,SINK=True):
        if EVEN<1 or ODD<1 or line<1:
            raise PolyError('Cannot create such a poly: negtive settings.')
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

        return
    def __getitem__(self,i):
        coord=self.num_to_coord(i)
        self.check_valid_coord(coord)
        return self.get_poly_by_coord(coord)

    def get_delta_pos_by_coord(self,coord):
        self.check_valid_coord(coord)
        x,y=coord
        if self.n==6:
            dx=x*(self.base_poly.points[0][0]-self.base_poly.points[4][0])
            dy=self.base_poly.rect[1]*(y+(x%2)*(self.EVEN-self.ODD)/2)
        elif self.n==8:
            dx=x*(self.base_poly.points[0][0]-self.base_poly.points[5][0])
            dy=(self.base_poly.rect[1]+self.base_poly.size)*(y+(x%2)*(self.EVEN-self.ODD)/2)
        return dx,dy
    def get_pos_by_coord(self,coord):
        sx,sy=self.base_poly.topleft
        dx,dy=get_delta_pos_by_coord(coord)
        return sx+dx,sy+dy
    def get_poly_by_coord(self,coord):
        dx,dy=self.get_delta_pos_by_coord(coord)
        return self.base_poly.copy_and_move((dx,dy))
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
        self.check_valid_coord(coord)
        x,y=coord
        neibors=[(x,y+1),(x,y-1),(x+1,y),(x-1,y),(x+1,y+((x%2)*2-1)*(self.EVEN-self.ODD)),(x-1,y+((x%2)*2-1)*(self.EVEN-self.ODD))]
        neibors=list(filter(self.is_valid_coord,neibors))
        return neibors
    def get_neibors_by_num(self,num):
        coord=self.num_to_coord(num)
        return(list(map(self.coord_to_num,self.get_neibors_by_coord(coord))))

