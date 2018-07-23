from poly import poly
from poly import PolyGroup,ComboGroup
import pygame
from pygame.locals import *
import time
pygame.init()
DIS=pygame.display.set_mode((200,200))
def main():
    base1=poly(n=6,r=40,topleft=(10,10))
    base2=poly(n=8,size=40,center=(100,140),lie=False)#True)
    FontObj=pygame.font.SysFont('stliti',20)
    for p in (base1,base2):
        pygame.draw.polygon(DIS,(255,255,255),p.points,2)
        x=0
        for i in p.points:
            text=FontObj.render(str(x),True,(0,255,255))
            _rect=text.get_rect()
            _rect.center=i
            DIS.blit(text,_rect)
            x+=1
        pygame.draw.rect(DIS,(255,255,5),p.rect.xywh,2)
    pygame.image.save(DIS,'demo_img2.jpg')
    pygame.display.update()
    while True:
        time.sleep(0.2)
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                return
main()
