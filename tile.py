# handling tiling hexagons and octagons
from . import poly
class PolyError(Exception):
    pass
class PolyGroup:
    def __init__(self,EVEN,ODD,line,base_hex,SINK=True):
        if EVEN<1 or ODD<1 or line<1:
            raise PolyError('Cannot create such a poly: negtive settings.')
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
        if not self.is_valid_coord(coord):
            raise IndexError('Index out of range')
        return self.get_poly_by_coord(coord)

    def get_pos_by_coord(self,coord):
        sx,sy=self.base_hex.topleft
        dx,dy=get_delta_pos_by_coord(coord)
        return sx+dx,sy+dy
    def get_poly_by_coord(self,coord):
        dx,dy=self.get_delta_pos_by_coord(coord)
        return self.base_hex.copy_and_move((dx,dy))
    def is_valid_coord(self,coord):
        x,y=coord
        if x>=self.line:
            return False
        if x%2==1 and y>=self.ODD:
            return False
        if x%2==0 and y>=self.EVEN:
            return False
        return True
    def num_to_coord(self,num):
        EVEN,ODD=self.EVEN_T,self.ODD_T
        p,q=divmod(num,(EVEN+ODD))
        #r,s=divmod(q,self.EVEN)
        r=min(1,q//EVEN)#r可能为2
        return p*2+r,q-r*EVEN
class HexGroup(PolyGroup):
    def get_delta_pos_by_coord(self,coord):
        if self.is_valid_coord(coord):
            x,y=coord
            #sx,sy=self.base_hex.topleft
            dx=x*(self.base_hex.points[0][0]-self.base_hex.points[4][0])
            dy=self.base_hex.rect[1]*(y+(x%2)*(self.EVEN-self.ODD)/2)
        return dx,dy
class OctGroup(PolyGroup):
    def get_delta_pos_by_coord(self,coord):

        if self.is_valid_coord(coord):
            x,y=coord
            dx=x*(self.base_hex.points[0][0]-self.base_hex.points[5][0])
            dy=(self.base_hex.rect[1]+self.base_hex.size)*(y+(x%2)*(self.EVEN-self.ODD)/2)
        return dx,dy
