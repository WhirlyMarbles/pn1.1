#%% imports and hide support prompt
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
pygame.init()

import assets

import pn1_1

import sys
#%%  locals

selected = None

minecraftia = assets.font
courier = assets.courier

def draw_text(lines, pos):
    for line in lines:
        screen.blit(courier.render(line, True, (255, 255, 255)), (pos[0], pos[1]))
        pos[1] += 40

class Tab:
    def __init__(self, title, image, hitbox):
        self.title = title
        self.icon = image
        self.color = (100, 100, 100)
        self.hitbox = hitbox
    def draw(self):
        pygame.draw.rect(screen, self.color, self.hitbox)
        screen.blit(minecraftia.render(self.title, True, (255, 255, 255)), (10, self.hitbox[1] + 20))

play = Tab("Play", assets.logo, pygame.Rect(0, 0, 250, 100))
settings = Tab("Settings", assets.settings, pygame.Rect(0, 100, 250, 100))
credits = Tab("Credits", assets.credits, pygame.Rect(0, 200, 250, 100))

selected = None

screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Picklenicker Launcher")
pygame.display.set_icon(assets.l_logo)

orange = (255, 165, 0)
gray = (100, 100, 100)

#%% main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_ESCAPE:
                selected = None
                play.color = gray
                settings.color = gray
                credits.color = gray
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            if play.hitbox.collidepoint(mousepos[0], mousepos[1]):
                selected = "play"
            if settings.hitbox.collidepoint(mousepos[0], mousepos[1]):
                selected = "settings"
            if credits.hitbox.collidepoint(mousepos[0], mousepos[1]):
                selected = "credits"
            if pygame.Rect(300, 300, 130, 70).collidepoint(mousepos[0], mousepos[1]) and selected == "play":
                pygame.quit()
                pn1_1.run(10)
                sys.exit()

    screen.fill((60, 60, 60))
    
    if selected == "play":
        play.color = orange
        settings.color = gray
        credits.color = gray
    if selected == "settings":
        play.color = gray
        settings.color = orange
        credits.color = gray
    if selected == "credits":
        play.color = gray
        settings.color = gray
        credits.color = orange
    
    
    play.draw()
    settings.draw()
    credits.draw()
    
    if selected == None:
        draw_text(["No tab selected"], [300, 300])
    if selected == "play":
        pygame.draw.rect(screen, (0, 190, 0), pygame.Rect(300, 300, 130, 70))
        screen.blit(minecraftia.render("PLAY", True, (255, 255, 255)), (310, 310))

    pygame.display.update()
# %% end