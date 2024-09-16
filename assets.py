import random

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "!"
import pygame
pygame.init()

pickles = [
    pygame.image.load(r"assets\images\pcls\netanyahu.png"),
    pygame.image.load(r"assets\images\pcls\ben_gvir.png"),
    pygame.image.load(r"assets\images\pcls\anxiety.png"),
]

player = pygame.transform.scale(pygame.image.load(r"assets\images\player.png"), (124, 158))
squidward = pygame.transform.scale(pygame.image.load(r"assets\images\squidward.png"), (64, 158))
powerup_squidward = pygame.image.load(r"assets\images\www.png")

logo = pygame.image.load(r"assets\images\logo.png")
l_logo = pygame.image.load(r"assets\images\launcherlogo.png")
pickle = pygame.image.load(r"assets\images\pickle.png")
bomb = pickle = pygame.image.load(r"assets\images\bomb.png")
credits = pygame.transform.scale(pygame.image.load(r"assets\images\credits.png"), (30, 30))
settings = pygame.transform.scale(pygame.image.load(r"assets\images\settings.png"), (30, 30))

button_overlay = pygame.image.load(r"assets/button_overlay.png")
button_overlay_hovered = pygame.image.load(r"assets/button_overlay_hovered.png")

heart = pygame.image.load(r"assets\images\heart.png")
noheart = pygame.image.load(r"assets\images\empty_heart.png")

walrus = pygame.image.load(r"assets/images/walrus.png")

explosion = pygame.image.load(r"assets\images\effects\explosion.png")

bgc = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

font = pygame.font.Font(r"assets\font.ttf", 36)
smallfont = pygame.font.Font(r"assets\font.ttf", 18)
titlefont = pygame.font.Font(r"assets\font.ttf", 100)
largefont = pygame.font.Font(r"assets\font.ttf", 56)
courier = pygame.font.SysFont(r"courier new", 36)

def scale_height(image, scaleby):
    return pygame.transform(image, (image.get_width() * scaleby, image.get_height() * scaleby))




schrodinger = pygame.image.load(r"assets/images/schrodingers_cat.png")