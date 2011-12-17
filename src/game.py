from settings import *
import pygame
import os, sys
from pygame.locals import *

SYSTEMPATH = sys.path[0]

def load_image(image, transparency = True, colorkey = (255, 0, 255)):
    """ Classic pygame loading image function :D """
    tmp = image.rsplit('/')
    tmp_file = os.path.join(SYSTEMPATH, tmp[0])
    for t_substr in tmp[1:]:
        tmp_file = os.path.join(tmp_file, t_substr)
    
    try:
        image_sur = pygame.image.load(tmp_file)
    except Exception:
        print 'Wrong image path buddy'
        raise SystemExit
    
    image_sur = image_sur.convert()
    if transparency:
        # The RLEACCEL is supposed to be faster on non-accelerated screens...not sure about that
        image_sur.set_colorkey(image_sur.get_at((0,0)), pygame.RLEACCEL) 
    
    return image_sur

def main():
    print 'Loading!'
    pygame.init()
    main_surface = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption(TITLE)
    guy_image = load_image('res/guy.png')
    while True:
        main_surface.fill(WHITE)
        main_surface.blit(guy_image, (50,50))
        pygame.display.update()
        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()
                exit()
    
if __name__ == '__main__':
    main()