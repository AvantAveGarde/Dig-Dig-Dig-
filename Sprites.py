#Sprites
from Settings import*
import pygame
vec = pygame.math.Vector2
from random import choice, randrange
from Settings import *

class Player(pygame.sprite.Sprite):
    #Player class
    def __init__(self, game):
        self.groups = game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames
        self.image.set_colorkey(BLACK)
        self.PLAYER_GRAV = PLAYER_GRAV
        self.infinite_jump = False
        self.dashing = False
        self.dash_reset = True
        
        #Position
        self.rect.center = (window_width / 2, window_height / 2)
        self.pos = vec(window_width / 2, window_height / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
    def load_frames(self):
        self.standing_frames = []
        self.walk_frames = []
        self.jump_frames = []


    def load_images(self):
        self.standing_frames = pygame.image.load("Miner.png")


        
        self.walk_frames_r = [self.game.player_spritesheet.get_image(8,8,42,58),
                              self.game.player_spritesheet.get_image(67,8,42,58),
                              self.game.player_spritesheet.get_image(127,8,42,58),
                              self.game.player_spritesheet.get_image(187,8,42,58),
                              self.game.player_spritesheet.get_image(8,80,42,58),
                              self.game.player_spritesheet.get_image(67,80,42,58),
                              self.game.player_spritesheet.get_image(127,80,42,58),
                              self.game.player_spritesheet.get_image(187,80,42,58),
                              self.game.player_spritesheet.get_image(8,151,42,58),
                              self.game.player_spritesheet.get_image(67,151,42,58)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))
        
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
                    
    def jump(self):
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if self.infinite_jump == True:
            self.game.jump.play()
            self.jumping = False
            self.vel.y = -PLAYER_JUMP
            
        elif hits and not self.jumping:
            self.game.jump.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def dashr(self):
        if (self.dashing == False) and (self.dash_reset == True):
            self.game.dash_sound.play()
            self.vel.x = PLAYER_JUMP * 1.5
            self.dashing = True
    def dashl(self):
        if (self.dashing == False) and (self.dash_reset == True):
            self.game.dash_sound.play()
            self.vel.x = -PLAYER_JUMP * 1.5
            self.dashing = True
        
        

    def update(self):
        self.animate()
        dash_hit = pygame.sprite.spritecollide(self, self.game.platforms, False)
        if dash_hit:
            self.dash_reset = True
            self.dashing = False
        
        self.acc = vec(0, self.PLAYER_GRAV)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC
    

        #Apply Friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #Kinematics
        self.vel += self.acc
        self.pos += self.vel + .5 * self.acc
        #wrap around the sides of the screen
        if self.pos.x > window_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = window_width
        
        self.rect.midbottom = self.pos

    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #Shows walking animation
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now + 20
                self.current_frame = (self.current_frame+1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.standing_frames

class Platform(pygame.sprite.Sprite):
    #Platform classes
    
    
    def __init__(self, game, x, y, s):

        self.groups = game.all_sprites, game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.PLATFORM_ACC = PLATFORM_ACC
        images = [self.game.bat_spritesheet.get_image(270, 0, 270, 60),
                  self.game.bat_spritesheet.get_image(330, 90, 140, 35),]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = -s

        
    def update(self):
        
        self.vel += self.PLATFORM_ACC
        self.rect.y += self.vel

class Boulder(pygame.sprite.Sprite):
    #Boulder classes
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image = pygame.image.load("boulder.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.vel = 3
        self.acc = PLAYER_GRAV
        self.vel += self.acc
        self.rect.y += self.vel

class Alerts(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image = pygame.image.load("warning.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

class Powerup(pygame.sprite.Sprite):
    def __init__(self, game):
        
        self.groups = game.all_sprites, game.powerups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.type = choice(['diamond', 'ruby', 'freeze', 'bomb','boots'])
        
        self.image = pygame.Surface((50, 50))
        if self.type == 'diamond':
            self.image = pygame.image.load("diamond2.png").convert_alpha()
        elif self.type == 'ruby':
            self.image = pygame.image.load("ruby2.png").convert_alpha()
        elif self.type == 'freeze':
            self.image = pygame.image.load("clock2.png").convert_alpha()
        elif self.type == 'bomb':
            self.image = pygame.image.load("bomb.png").convert_alpha()
        elif self.type == 'boots':
            self.image = pygame.image.load("boots2.png").convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([window_width /4, window_width /2, window_width * 3 / 4, window_width / 3, window_width * 2 / 3])
        self.rect.centery = (window_height + 100)
        

    def update(self):
        self.vel = -POWERUP_SPEED
        self.acc = -PLAYER_GRAV
        self.vel += self.acc
        self.rect.y += self.vel

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("test2.jpg").convert()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()
        
    def get_image(self, x, y, width, height):
        # grab a image out of a large spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        return image
        
class Mob(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        self.image = pygame.Surface((70, 40))
        
        self.imageL_up = self.game.bat_spritesheet.get_image(0, 0, 70, 40)
        self.imageL_up.set_colorkey(BLACK)

        self.imageL_down = self.game.bat_spritesheet.get_image(190, 0, 55, 40)
        self.imageL_down.set_colorkey(BLACK)

        self.imageR_up = self.game.bat_spritesheet.get_image(180, 95, 70, 40)
        self.imageR_up.set_colorkey(BLACK)

        self.imageR_down = self.game.bat_spritesheet.get_image(95, 185, 55, 40)
        self.imageR_down.set_colorkey(BLACK)

        self.image = self.imageL_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, window_width + 100])
        
        
        self.vx = randrange(1, 4)
        if self.rect.centerx > window_width:
            self.vx *= -1
        self.rect.y = choice([window_height /4,window_height/ 2, window_height - 200])
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1

        center = self.rect.center
        if self.dy < 0 and self.vx > 0:
            self.image = self.imageL_up
        elif self.dy > 0 and self.vx > 0:
            self.image = self.imageL_down
        elif self.dy < 0 and self.vx < 0:
            self.image = self.imageR_up
        elif self.dy > 0 and self.vx < 0:
            self.image = self.imageR_down
            
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        
        if self.rect.left > window_width + 100 or self.rect.right < -100:
            self.kill()
        
