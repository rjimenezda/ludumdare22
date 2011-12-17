from settings import *
import pygame
import os, sys
from pygame.locals import *
import math
import copy

SYSTEMPATH = sys.path[0]

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = load_image('res/bullet.png')
        self.rect = pygame.rect.Rect(-1, -1, 0, 0)
        self.xdir = 1.0
        self.ydir = 1.0
        self.speed = 15
        self.fired = False
    
    def update(self):
        if self.fired:
            self.rect.x += self.xdir * self.speed
            self.rect.y += self.ydir * self.speed
        
    def fire(self, position, pRotation):
        self.fired = True
        self.xdir = math.cos(math.radians(pRotation + 90))
        self.ydir = -math.sin(math.radians(pRotation + 90))
        self.rect = copy.copy(position)
        self.rect.x = self.rect.centerx
        self.rect.y = self.rect.centery

class Guy():
    def __init__(self): 
        self.crosshairdist = 20
        self.surface = pygame.Surface((32, 32 + 16 + self.crosshairdist))
        self.surface.fill(WHITE)
        self.image = load_image('res/guy.png')
        self.crosshair = load_image('res/crosshair1.png')
        self.surface.blit(self.image, (0, 16 + self.crosshairdist))
        self.surface.blit(self.crosshair, (8,0))
        self.original_image = self.surface 
        self.position = self.surface.get_rect()
        self.position.centery -= 16
        self.position.move_ip(RESOLUTION[0] / 2, RESOLUTION[1] / 2)
        
#        self.bullet = load_image('res/bullet.png')
#        self.bullet_pos = self.bullet.get_rect()
#        self.bullet_pos.centerx = self.position.centerx
#        self.bullet_pos.centery = self.position.centery
        
        self.speed = 3
        self.rotateSpeed = 5
        self.rotated = 0
    
    def moveGuy(self, keys):
        if keys[left]:
            self.position[0] -= self.speed
        if keys[right]:
            self.position[0] += self.speed
        if keys[up]:
            self.position[1] -= self.speed
        if keys[down]:
            self.position[1] += self.speed
            
#        if keys[K_SPACE]:
#            self.bullet_pos.x += math.cos(math.radians(self.rotated + 90)) * 10
#            self.bullet_pos.y += -math.sin(math.radians(self.rotated + 90)) * 10
        
    
    def rotateGuy(self, keys):
        if keys[K_LEFT]:    
            self.rotated += self.rotateSpeed
        if keys[K_RIGHT]:    
            self.rotated -= self.rotateSpeed
            
        if self.rotated >= 360:
            self.rotated = 0
        elif self.rotated <= -360:
            self.rotated = 360
        
        rect_center = self.position.center
        self.surface = pygame.transform.rotate(self.original_image, self.rotated)
        self.position = self.surface.get_rect()
        self.position.center = rect_center
        
            
def load_image(image, transparency = True, colorkey = (255, 0, 255)):
    """ Classic pygame loading image function :D """
    
    # Silly windows, you need extra code to load files
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
    pygame.init()
    main_surface = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption(TITLE)
    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)
    fpsTimer = pygame.time.Clock()
#    pygame.mouse.set_visible(False)
    guy = Guy()
    bullet = Bullet(guy)
    while True:
        # Render code 
        main_surface.fill(WHITE)
        main_surface.blit(guy.surface, guy.position)
        main_surface.blit(bullet.image, bullet.rect)
        
        
        # Update code
        bullet.update()
        
        # Has to be called outside, could be called multiple times
        guy.moveGuy(pygame.key.get_pressed())
        guy.rotateGuy(pygame.key.get_pressed())
        # Input code
        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()
                exit()
            elif evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                if evt.key == K_SPACE:
                    bullet.fire(guy.position, guy.rotated)

        pygame.display.update()
        fpsTimer.tick(TARGET_FPS)
    
if __name__ == '__main__':
    main()