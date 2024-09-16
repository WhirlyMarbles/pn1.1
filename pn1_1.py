"""
Hello to every future readers!
I am happy to display the newest update to the beloved and (still) authentically random Picklenicker!

Introducing:
————————————————
PICKLNICKER 1.1!
————————————————

This is just a revamp for the code. This version implements Python classes,
and more advanced loops.

More info can be found in the README folder.

Thank you!

"""


#%%
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
pygame.init()

import assets

import sys
import random
import math
import time

SW = 1000
SH = 600

skyblue = (135, 206, 235)

screen = pygame.display.set_mode((SW, SH), pygame.RESIZABLE)
pygame.display.set_caption("Picklenicker 1.1")
pygame.display.set_icon(assets.logo)

font = assets.font

#%% Important classes
class WWW:
    def __init__(self):
        self.image = assets.powerup_squidward
        self.pos = [random.randint(0, SW - self.image.get_width()), random.randint(100, 200) * -1]
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
        self.width, self.height = self.image.get_width(), self.image.get_height()
    def draw(self, newpos=[]):
        if not newpos:
            newpos = self.pos
        self.x, self.y = newpos
        self.hitbox.topleft = newpos
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox)
        screen.blit(self.image, newpos)

class Pickle:
    def __init__(self, pickle, multiplier, speed, x=None, y=None):
        self.image = pygame.transform.scale(pickle, (pickle.get_width() * multiplier,
                                                     pickle.get_height() * multiplier))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        if x == None and y == None:
            x = random.randint(0, SW - self.width)
            y = 0 - random.randint(200, 800)#for some reason the random.randint function doesnt work with negative integers (but it does for zero)
        self.hitbox = pygame.Rect(x, y, self.width, self.height)
        self.pos = [x, y]
        self.x = x
        self.y = y
        self.speed = speed
    
    def draw(self, newpos=[]):
        if not newpos:
            newpos = self.pos
        self.x, self.y = newpos
        self.hitbox.topleft = newpos
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox)
        screen.blit(self.image, newpos)

class Player:
    def __init__(self, image):
        self.speed = 6
        self.image = image
        self.x = SW / 2 - image.get_width() / 2
        self.y = SH - image.get_height()
        self.width = image.get_width()
        self.height = image.get_height()
        self.pos = [self.x, self.y]
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
        self.direction = None
        self.hp = 10
        self.immune = False
    
    def squidward(self):
        self.immune = True
        self.image = assets.squidward
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], assets.squidward.get_width(), assets.squidward.get_height())
    def unsquidward(self):
        self.immune = False
        self.image = assets.player
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], assets.player.get_width(), assets.player.get_height())


    def draw(self, newpos=[]):
        if not newpos:
            newpos = self.pos
        self.x, self.y = newpos
        self.hitbox.topleft = newpos
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox)
        screen.blit(self.image, newpos)


keyassign = {
        pygame.K_RIGHT: "right",
        pygame.K_LEFT: "left",
        pygame.K_d: "right",
        pygame.K_a: "left",
        pygame.K_t: "toggle debug",
        pygame.K_b: "stop",
        pygame.K_ESCAPE: "stop",
        pygame.K_p: "pause"
}
debug = False

def gen_pickles(pickles):
    pickles_list = []
    for pickle in range(pickles):
        pickles_list.append(
            Pickle(
            random.choice(assets.pickles),
            random.randint(50, 100) / 75,
            random.randint(2, 3)
            )
        )
    return pickles_list

def hitbox_intersect(box_a, box_b): # gets two pygame.Rect objects
    intersect_x = False
    intersect_y = False
    if box_a.x > box_b.x and box_a.x < box_b.x + box_b.width:
        intersect_x = True

    if box_b.x > box_a.x and box_b.x < box_a.x + box_a.width:
        intersect_x = True

    if box_a.y > box_b.y and box_a.y < box_b.y + box_b.height:
        intersect_y = True

    if box_b.y > box_a.y and box_b.y < box_a.y + box_a.height:
        intersect_y = True

    if intersect_x and intersect_y:
        return True
    return False

def run(pickles):
    global debug
    global SW
    global SH
    player = Player(assets.player)
    
    buttonplay = pygame.Rect(200, 300, 128, 70)
    running = True
    playtext = font.render("PLAY", True, (50, 50, 50))
    title = assets.titlefont.render("PICKLENICKER", True, (50, 50, 50))
    while running:
        mousepos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_b, pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonplay.collidepoint(mousepos[0], mousepos[1]):
                    running = False
            if event.type == pygame.VIDEORESIZE:
                SW, SH = event.size
            
        if buttonplay.collidepoint(mousepos[0], mousepos[1]):
            buttonplayimage = assets.button_overlay_hovered
        else:
            buttonplayimage = assets.button_overlay
        screen.fill(skyblue)
        screen.blit(pygame.transform.rotate(buttonplayimage, math.sin(time.time()) * 10), (200, 300))
        screen.blit(pygame.transform.rotate(playtext, math.sin(time.time()) * 10), (210, 310))
        screen.blit(title, (146, 50))
        pygame.display.update()



    pickles = gen_pickles(pickles)

    powerup = WWW()

    x = player.x
    y = player.y

    score = 0

    todo = []
    tickengine = pygame.time.Clock()

    speed = 0

    squidwardtime = 0
    
    while True:
        tickrate = 100
        if player.hp == 0:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_RETURN:
                            return "dead"
                screen.fill((0, 0, 0))

                youdied = font.render(f"You died! Press ENTER to retry", True, (255, 0, 0))
                scorestr = font.render(f"Score: {str(score)}", True, (255, 0, 0))
                screen.blit(youdied, (30, 30))
                screen.blit(scorestr, (30, 200))

                pygame.display.update()

        # TPS boosting {
        todo = list(set(todo))
        # }
        # why do you how come do you ask?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                try:
                    todo.append(keyassign[event.key])
                except KeyError:
                    pass
            if event.type == pygame.VIDEORESIZE:
                SW, SH = event.size
        for item in todo:
            if item == "right":
                player.direction = "right"
            if item == "left":
                player.direction = "left"
            if item == "toggle debug":
                debug = not debug
            if item == "stop":
                pygame.quit()
                sys.exit()
            if item == "pause":
                paused = True
                overlay = pygame.Surface((SW, SH), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                screen.blit(overlay, (0, 0))
                screen.blit(font.render("PAUSED", True, (0, 0, 0)), ((10, 20)))
                pygame.display.update()
                while paused:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_b:
                                pygame.quit()
                                sys.exit()
                            if event.key == pygame.K_p:
                                paused = False

            todo.remove(item)

        if player.direction == "right":
            x += player.speed
        if player.direction == "left": # i just put a comment here for no reason at all
            x -= player.speed
        if player.x > SW and player.direction == "right":
            x = 0 - player.width
        if player.x + player.width < 0 and player.direction == "left":
            x = SW
        y = SH - player.height
        screen.fill(assets.bgc)
        for pickle in pickles:
            if pickle.y > SH:
                pickle.draw([random.randint(0, SW - pickle.width), 0 - random.randint(300, 600)])
                if not player.immune:
                    player.hp -= 1
            if hitbox_intersect(player.hitbox, pickle.hitbox):
                pickle.draw([random.randint(0, SW - pickle.width), 0 - random.randint(300, 600)])
                score += pickle.width
            pickle.draw([pickle.x, pickle.y + pickle.speed])
        
        powerup.draw([powerup.x, powerup.y + 1])
        if hitbox_intersect(player.hitbox, powerup.hitbox):
            powerup.draw([random.randint(0, SW - powerup.width), 0 - random.randint(300, 600)])
            squidwardtime = 600

        # render hp
        penx = 0
        for i in range(player.hp):
            screen.blit(assets.heart, (penx, 0))
            penx += 16
        for i in range(10 - player.hp):
            screen.blit(assets.noheart, (penx, 0))
            penx += 16
        # render score
        scorestr = font.render(str(score), True, (255, 0, 0))
        screen.blit(scorestr, (SW - scorestr.get_width(), 0))

        if squidwardtime:
            player.squidward()
        else:
            player.unsquidward()
        player.draw([x, y])
        tickengine.tick(int(tickrate))
        tickrate += 0.1
        pygame.display.update()
        if squidwardtime > 0:
            squidwardtime -= 1
#%% end
while True:
    if run(10) == "dead":
        pass