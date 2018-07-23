from poly import poly
from poly import PolyGroup,ComboGroup
import pygame
from pygame.locals import *
import time
pygame.init()
DIS=pygame.display.set_mode((500,500))
def main():
    base1=poly(n=6,r=40,topleft=(50,50))
    base3=poly(n=6,r=40,topleft=(50,270))
    base2=poly(n=8,r=40,topleft=(250,50))
    pg=ComboGroup((PolyGroup(base_poly=base1,EVEN=3,ODD=2,line=3),\
                PolyGroup(base_poly=base3,EVEN=3,ODD=2,line=3),\
                PolyGroup(base_poly=base2,EVEN=3,ODD=2,line=3)))
    FontObj=pygame.font.SysFont('stliti',20)
    x=0
    for g in pg.groups:
        for p in g:
            pygame.draw.polygon(DIS,(255,255,255),p.points,2)
            text=FontObj.render(str(x),True,(0,255,255))
            _rect=text.get_rect()
            _rect.center=p.center
            DIS.blit(text,_rect)
            x+=1
        print(g.rect.xywh)
        pygame.draw.rect(DIS,(255,255,255),g.rect.xywh,2)
    pygame.image.save(DIS,'demo_img1.jpg')
    pygame.display.update()
    while True:
        time.sleep(0.2)
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                return
            if event.type==MOUSEBUTTONDOWN:
                po=pg.collide(event.pos)
                print(pg.get_neibors_by_num(pg.coord_to_num(po)))
                print(po)
main()
