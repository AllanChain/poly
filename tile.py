# handling tiling hexagons and octagons
from . import poly

class HexGroup:
    def __init__(self,EVEN,ODD,line,base_hex):
        self.__dict__.update(locals())
        del self.__dict__['self']
        return
    def __getitem__(self,i):
        coord=self.num_to_coord(i)
        if not self.is_valid_coord(coord):
            raise IndexError('Index out of range')
        return self.get_poly_by_coord(coord)
    def get_delta_pos_by_coord(self,coord):
        x,y=coord
        #sx,sy=self.base_hex.topleft
        dx=x*(self.base_hex.points[0][0]-self.base_hex.points[4][0])
        dy=self.base_hex.rect[1]*(y+(x%2)*(self.EVEN-self.ODD)/2)
        return dx,dy
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
        p,q=divmod(num,(self.EVEN+self.ODD))
        #r,s=divmod(q,self.EVEN)
        r=min(1,q//self.EVEN)#r有可能为2
        return p*2+r,q-r*self.EVEN

