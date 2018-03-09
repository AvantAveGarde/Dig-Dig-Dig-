#Framework.py
#Colton Lee
#Spring 2017

#Initialization Settings
import pygame, sys
from Settings import *
import random

if (__name__ == "__main__"):
    #Window / Sprite Setup
    pygame.init()
    pygame.mixer.init()

    #pygame.mixer.music.load("main_theme.ogg")
    #pygame.mixer.music.play(1, 0.0)

    running = True
    
    all_sprites = pygame.sprite.Group()
    
    window = pygame.display.set_mode((window_resolution))
    pygame.display.set_caption("Demo")
    
    #Loads fps limiter into the game, limits GPU usage.
    clock = pygame.time.Clock()



    #Allows us to exit the program
    while(running):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
        window.fill(GREY)


    #1 Update Functions It is important that these go in order.

        
    #2 Logic Testing

        
    #3 Draw Everything

        
    #4 Delay Framerate
        clock.tick(frames_per_second)
        
    #5 Update The Screen
        pygame.display.update()
        
    pygame.quit()
    sys.exit()
        
        
        
