from settings import *
import pygame
import os, sys
from pygame.locals import *

SYSTEMPATH = sys.path[0]

class Guy():
    
    def __init__(self):
        self.position = [0,0]
        self.image = load_image('res/guy.png')
        self.speed = 3
    
    def moveGuy(self, keys):
        # This doesn't work great
        if keys[left]:
            self.position[0] -= self.speed
        if keys[right]:
            self.position[0] += self.speed
        if keys[up]:
            self.position[1] -= self.speed
        if keys[down]:
            self.position[1] += self.speed
            
def load_image(image, transparency = True, colorkey = (255, 0, 255)):
    """ Classic pygame loading image function :D """
    
    # Silly windows, you need extra code to load images
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
        # The RLEACCEL is supposed to be faster on non-accelerated screens...not sure why :P
        image_sur.set_colorkey(image_sur.get_at((0,0)), pygame.RLEACCEL) 
    
    return image_sur

def getCrosshairPosition(playerPosition):
    return (60,60)    

def main():
    print 'Loading!'
    pygame.init()
    main_surface = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption(TITLE)
    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)
    fpsTimer = pygame.time.Clock()
    crosshair = load_image('res/crosshair1.png')
#    pygame.mouse.set_visible(False)
    guy = Guy()
    guy_image = load_image('res/guy.png')
    while True:
        # Render code 
        main_surface.fill(WHITE)
        main_surface.blit(guy.image, guy.position)
        main_surface.blit(crosshair, getCrosshairPosition('lol'))
        
        # Has to be called outside, could be called multiple times
        guy.moveGuy(pygame.key.get_pressed())
        # Input code
        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()
                exit()
            elif evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    pygame.quit()
                    exit()
            
        pygame.display.update()
        fpsTimer.tick(TARGET_FPS)
    
if __name__ == '__main__':
    main()