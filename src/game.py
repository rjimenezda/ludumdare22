from settings import *
import pygame
import os, sys
from pygame.locals import *
import math
import copy

SYSTEMPATH = sys.path[0]
           
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = load_image('res/bullet.png')
        self.original_image = self.image
        self.rect = pygame.rect.Rect(-1, -1, 0, 0)
        self.xdir = 1.0
        self.ydir = 1.0
        self.speed = 15
        self.fired = False
    
    def update(self):
        if self.fired:
            self.rect.x += self.xdir * self.speed
            self.rect.y += self.ydir * self.speed
        elif self.fired:
            self.rect = copy.copy(self.player.rect)
                
    def fire(self):
        self.fired = True
        self.xdir = math.cos(math.radians(self.player.rotated + 90))
        self.ydir = -math.sin(math.radians(self.player.rotated + 90))
        self.rect = copy.copy(self.player.rect)
        
        rect_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.player.rotated)
        self.rect = self.image.get_rect()
        self.rect.center = rect_center

class Guy():
    def __init__(self): 
        self.image = load_image('res/guy.png')
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.move_ip(RESOLUTION[0] / 2, RESOLUTION[1] / 2)
        self.radius = 32
    
        self.speed = 3
        self.rotateSpeed = 5
        self.rotated = 0
    
    def moveGuy(self, keys):
        if keys[left]:
            self.rect[0] -= self.speed
        if keys[right]:
            self.rect[0] += self.speed
        if keys[up]:
            self.rect[1] -= self.speed
        if keys[down]:
            self.rect[1] += self.speed
        
    
    def rotateGuy(self, keys):
        if keys[K_LEFT]:    
            self.rotated += self.rotateSpeed
        if keys[K_RIGHT]:    
            self.rotated -= self.rotateSpeed
            
        if self.rotated >= 360:
            self.rotated = 0
        elif self.rotated <= -360:
            self.rotated = 360
        
        rect_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.rotated)
        self.rect = self.image.get_rect()
        self.rect.center = rect_center

def getCrosshairPosition(playerPosition):
    return (60,60)    

def main():
    pygame.init()
    pygame.mixer.init()
    main_surface = pygame.display.set_mode(RESOLUTION)
    badguy = load_image('res/badguy.png')
    helper = load_image('res/helper.png')
    origbadguy = badguy
    orighelper = helper
    background_image = load_image('res/background.png', False)
    pygame.display.set_caption(TITLE)
    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)
    fpsTimer = pygame.time.Clock()
#    pygame.mouse.set_visible(False)
    guy = Guy()
    bullet = Bullet(guy)
    sndindex = 0
    bulletsnds = [pygame.mixer.Sound('res/shot1.wav'), pygame.mixer.Sound('res/shot2.wav')] 
    while True:
        # Render code 
        main_surface.blit(background_image, (0,0))
        pygame.draw.circle(main_surface, (255, 210, 0), guy.rect.center, guy.radius)
        main_surface.blit(bullet.image, bullet.rect)
        main_surface.blit(guy.image, guy.rect)  
        main_surface.blit(badguy, (50,50))
        main_surface.blit(helper, (500,500))
        
        # Update code
        bullet.update()
        badguy = pygame.transform.rotate(origbadguy, guy.rotated)
        helper = pygame.transform.rotate(orighelper, guy.rotated)
        
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
                    bullet.fire()
                    bulletsnds[sndindex].stop()
                    sndindex += 1
                    bulletsnds[sndindex].play()
                    if (sndindex == 1):
                        sndindex = 0
                    guy.radius += 1

        pygame.display.update()
        fpsTimer.tick(TARGET_FPS)
    
if __name__ == '__main__':
    main()