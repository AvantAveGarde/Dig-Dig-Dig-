#Final.py
#Colton Lee, Maria, Keneth
#Spring 2017

#Initialization Settings
import pygame, sys
from Settings import *
from Sprites import *
import random
import time


from os import path

class Game:
    def __init__(self):
        #Initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.window = pygame.display.set_mode((window_resolution))
        pygame.display.set_caption("Demo")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(font_name)
        self.load_data()
        
        
        
    def load_data(self):
        #Loads the high score and saves if you reach a higher one.
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'spritesheets')
        with open(path.join(self.dir, HS_FILE), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
                
        #Load Images
        self.bat_spritesheet = Spritesheet(path.join(img_dir, BAT_SPRITESHEET))
        self.player_spritesheet = Spritesheet(path.join(img_dir, PLAYER_SPRITESHEET))
        
                
        #load sound
        self.snd_dir = path.join(self.dir, 'snd')
        
        self.freeze_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'za_warudo.wav'))

        self.explosion_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'the_hand.wav'))
        self.coin_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'coin.wav'))
        self.jump = pygame.mixer.Sound(path.join(self.snd_dir, 'jump.wav'))
        self.dash_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'dash2.wav'))
        self.boots_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'powerup.wav'))
        self.stomp_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'stomp.wav'))
    def new(self):
        #Launch a new game
        pygame.mixer.music.load("main_theme.ogg")
        pygame.mixer.music.play(10, 0.0)
        pygame.mixer.music.set_volume(0.2)
        
        self.all_sprites = pygame.sprite.Group()
        
        self.platforms = pygame.sprite.Group()
        
        self.boulders = pygame.sprite.Group()

        self.warnings = pygame.sprite.Group()

        self.mobs = pygame.sprite.Group()
        
        

        self.powerups = pygame.sprite.Group()
        
        self.player = Player(self)
        
        
        
        self.score = 0
        self.count = 0
        self.mob_timer = 0
        self.powerup_timer = 0
        self.powerup_duration = 0
        self.frozen = False
        self.infjump = False
        self.PLATFORM_FREEZE = PLATFORM_FREEZE
        self.platform_count = 10
        self.med_plat_count = 0
        

        
        
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
            
            
        for warn in WARNING_LIST:
            w = _Warning(*warn)
            self.all_sprites.add(w)
            self.warnings.add(w)

        
        self.BG = Background(0, 0)
        
        self.run()
        
        
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(frames_per_second)
            self.events()
            self.update()
            self.draw()
            
    def update(self):
        # Game Loop Updater
        pygame.display.update()
        self.all_sprites.update()
        
        #Remove these later, they will fix the speeds of everything
        self.platforms.update()
        self.boulders.update()
        self.warnings.update()

        PLATFORM_SPEED = 0

        #Mob Spawns
        now = pygame.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            if self.frozen == True:              
                Mob(self)
                for mob in self.mobs:
                    mob.vx = 0
            else:
                Mob(self)    
            self.powerup_duration += 1
            
        if now - self.powerup_timer > 15000 + random.choice([-2500, -1500, 0, 1500, 2500]):
            self.powerup_timer = now
            Powerup(self)
            
        #Platform collider
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top + 1
                    self.player.vel.y = 0
                    self.player.jumping = False
        if self.player.vel.y < 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.rect.top = hits[0].rect.bottom + 1
                self.player.vel.y = 0
            
                
        
        
        #Deletes platforms as they reach the top of the screen
        for plat in self.platforms:
            if plat.rect.top <= 0:
                plat.kill()
                self.score += 10
                
        for boulder in self.boulders:
            if boulder.rect.top >= window_height:
                boulder.kill()
                self.score += 50
                for warning in self.warnings:
                    warning.kill()
        for powerup in self.powerups:
            if powerup.rect.top <= 0:
                powerup.kill()
                

        #random platform generator
        while len(self.platforms) < self.platform_count:
            width = random.randrange(100, 200)
            spawn_boulders = True
            Platform(    self,
                         choice(RANDOM),
                         random.randrange(window_height, window_height + 200),
                         PLATFORM_SPEED
                    )
            if self.score >= 500:
                while self.med_plat_count < 1:
                    Platform(
                             self,
                             choice(RANDOM),
                             random.randrange(window_height, window_height + 200),
                             1.125
                            )
                    self.med_plat_count += 1
                if self.score >= 1000:
                    pass
            
            if self.count == 12 and spawn_boulders == True:
                #x, y, w, h
                self.boulder_x = random.randrange(0, window_width - width)
                
                b = Boulder(self.boulder_x,
                            random.randrange(-700, -500),
                            100, 100)
                w = Alerts(self.boulder_x + 10, 10, 50, 50)
                
                self.warnings.add(w)
                self.boulders.add(b)
                self.all_sprites.add(b)
                self.all_sprites.add(w)
                self.count = 0
                
                
                if self.score >= 1000 and spawn_boulders == True:
                    self.boulder2_x = random.randrange(0, window_width - width)
                    b = Boulder(self.boulder2_x, random.randrange(-500, -300), 100, 100)
                    w = Alerts(self.boulder2_x + 10, 10, 50, 50)
                    
                    self.warnings.add(w)
                    self.boulders.add(b)
                    self.all_sprites.add(b)
                    self.all_sprites.add(w)
                    self.count = 0
                    self.platform_count = 9
                    
                    
                    
                
                if self.score >= 2000 and spawn_boulders == True:
                    self.boulder3_x = random.randrange(0, window_width - width)
                    b = Boulder(self.boulder3_x, random.randrange(-500, -300), 100, 100)
                    w = Alerts(self.boulder3_x + 10, 10, 50, 50)
                    
                    self.warnings.add(w)
                    self.boulders.add(b)
                    self.all_sprites.add(b)
                    self.all_sprites.add(w)
                    self.count = 0
                    self.platform_count = 8
                    

            self.count = self.count + 1
            self.med_plat_count = 0
            self.fast_plat_count = 0

        #Kill functions, need to implement a health / life system
        if self.player.rect.bottom > (window_height + 150):
            for sprite in self.all_sprites:
                sprite.kill()
                self.playing = False
                    
        if self.player.rect.top <= -35:
            for sprite in self.all_sprites:
                sprite.kill()
                self.playing = False
                
        boulder_collide = pygame.sprite.spritecollide(self.player, self.boulders, False)
        if boulder_collide:
            self.player.kill()
            self.playing = False

        
        
        
        mob_collide = pygame.sprite.spritecollide(self.player, self.mobs, False)
        
        for mob in mob_collide:
            if self.player.rect.bottom < (mob.rect.top + 25):
                mob.kill()
                self.stomp_sound.play()
                self.score += 100
                self.player.vel.y = -PLAYER_JUMP / 2
            elif self.player.rect.bottom > (mob.rect.top):
                self.player.kill()
                self.playing = False

        

        powerup_collide = pygame.sprite.spritecollide(self.player, self.powerups, False)
        if powerup_collide:
            if powerup.type == 'ruby':
                
                self.coin_sound.play()
                self.score += 100
            elif powerup.type == 'diamond':
                
                self.coin_sound.play()
                self.score += 200
            elif powerup.type == 'freeze':
                
                for platform in self.platforms:
                    platform.PLATFORM_ACC = self.PLATFORM_FREEZE
                    platform.vel = 0
                for mob in self.mobs:
                    mob.vx = 0
                
                for boulder in self.boulders:
                    boulder.kill()
                self.freeze_sound.play()
                self.powerup_duration = 0
                self.frozen = True
                
                
            elif powerup.type == 'boots':
                self.boots_sound.play()
                self.powerup_duration = 0
                self.player.infinite_jump = True
                self.infjump = True
                
            elif powerup.type == 'bomb':
                
                self.explosion_sound.play()
                for mob in self.mobs:
                    mob.kill()
                    self.score += 50
            
            for powerup in self.powerups:
                powerup.kill()
            for boulder in self.boulders:
                boulder.kill()
            for warning in self.warnings:
                warning.kill()
            
        if len(self.platforms) == 0:
            self.playing = False

        if (self.frozen == True) and (self.powerup_duration > 1):
            for platform in self.platforms:
                platform.PLATFORM_ACC = PLATFORM_ACC
            for mob in self.mobs:
                mob.vx = randrange(1, 4)
            self.frozen = False
            
        if (self.infjump == True) and (self.powerup_duration > 1):
            self.player.infinite_jump = False
                
            
    def events(self):
        # Game Loop - Events
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                if self.playing:
                    self.playing = False
                self.running = False

            # Jump function
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    self.player.jump()
                    
                if event.key == pygame.K_e:
                    self.player.dashr()
                if event.key == pygame.K_q:
                    self.player.dashl()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    self.player.jump_cut()
                    
        
    def draw(self):
        # Draw function
        
        self.window.fill(GREY)
        self.window.blit(self.BG.image, self.BG.rect)
        self.all_sprites.draw(self.window)
        self.draw_text(str(self.score), 22, WHITE, window_width / 2, 0)
        pygame.display.flip()
        


    def show_start_screen(self):
        # Start Screen
        self.window.fill(WHITE)
        self.draw_text("Dig! Dig! Dig!", 48, BLACK, window_width / 2, window_height / 4)
        self.draw_text("WASD to move, SPACE to Jump, Q and E to Dash", 22, BLACK, window_width /2, window_height / 2)
        self.draw_text("Press 'Y' Key to Play", 22, BLACK, window_width / 2, window_height * 3 / 4)
        self.draw_text("Highscore: " + str(self.highscore), 22, BLACK, window_width / 2, 15)
        self.draw_text("Credits:", 22, BLACK, 100, 0)
        self.draw_text("EAE - Gamecraft", 22, BLACK, 100, 20)
        self.draw_text("Colton Lee", 22, BLACK, 100, 40)
        self.draw_text("Maria Reis", 22, BLACK, 100, 60)
        self.draw_text("Kenneth Pangilinan", 22, BLACK, 100, 80)
        self.window.blit(pygame.image.load("Logo.png"), (1000, 500))
                       
        pygame.display.flip()

        self.wait_for_key()

    def show_game_over_screen(self):
        # Game Over / Continue
        if not self.running:
            return
        
        self.window.fill(WHITE)
        self.draw_text("GAME OVER", 48, BLACK, window_width / 2, window_height / 4)
        self.draw_text("Score: " + str(self.score), 22, BLACK, window_width /2, window_height / 2)
        self.draw_text("Press 'Y' Key to Play Again or 'N' to Return to Menu", 22, BLACK, window_width / 2, window_height * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!!!", 22, BLACK, window_width / 2, window_height / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'r+') as f:
                f.write(str(self.score))
        else:
            self.draw_text("Highscore: " + str(self.highscore), 22, BLACK, window_width / 2, 15)
                      
        pygame.display.flip()
        self.wait_for_key()

    #If you press the 'y' button, start the game
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(frames_per_second)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_y:
                        waiting = False
                    elif event.key == pygame.K_n:
                        go.show_start_screen()

    #Draws all the text stuff, title, screen
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.window.blit(text_surface, text_rect)

go = Game()
go.show_start_screen()

#Allows us to exit the program
while(go.running):
    go.new()
    go.show_game_over_screen()

pygame.quit()
sys.exit()
        
        
        
