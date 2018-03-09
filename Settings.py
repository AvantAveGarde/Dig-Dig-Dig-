#Colours.py
#Colton Lee, Maria, Keneth
#Spring 2017
#This page will hold all of our variables, any changes for platform speed,
#player speed, etc. can be adjusted here.

import pygame

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
GREY  = pygame.Color(150, 150, 150)
RED   = pygame.Color(255, 0, 0)
GREEN   = pygame.Color(0, 255, 0)
BLUE   = pygame.Color(0, 0, 255)
PINK = pygame.Color(255, 105, 180)
YELLOW = (255, 255, 0)

HS_FILE = "highscore.txt"
BAT_SPRITESHEET = "Bat.png"
PLAYER_SPRITESHEET = "MinerWalking.png"

frames_per_second = 60
window_resolution = window_width, window_height = 1280, 720
font_name = 'arial'

#Player Properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5
PLAYER_JUMP = 15

#Game Properties
POWERUP_SCORE = 100
POWERUP_SPAWN_PCT = 5
POWERUP_SPEED = 2
FREEZE_SPEED = -1

#Mob spawn Properties
MOB_FREQ = 5000

#Platform Properties
PLATFORM_ACC = -0.00001 #Platform acceleration
PLATFORM_FREEZE = 0

PLATFORM_SPEED = 0
RANDOM = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 100, 1100, 1200,
          
         ]

                #x, y, width, height
PLATFORM_LIST = [
    
                 (0, 100, PLATFORM_SPEED),
                 (640, 680, PLATFORM_SPEED),
                 (800, 570,PLATFORM_SPEED),
                 (125, 300,             PLATFORM_SPEED),
                 (350, 200,                             PLATFORM_SPEED),
                 (175, 100,                             PLATFORM_SPEED),
                 (400, 500,PLATFORM_SPEED),
                 (640, 400, PLATFORM_SPEED),
                 
                 ]

BOULDER_LIST = []
WARNING_LIST = []

