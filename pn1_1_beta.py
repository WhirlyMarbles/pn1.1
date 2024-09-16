r"""
Hello to every future readers!
I am happy to display the newest update to the beloved and (still) authentically random Picklenicker!

Introducing:
/————    ———    —\   
|PICK————KER————!|
\————LNIC——— 1.1—/
     ————   ————  

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

# settings
import json
if not os.path.isfile("assets/picklnicker.json"):
    picklnickerjsontemplate = """{
  "highscore": 0,
  "difficulty": "normal",
  "bgcolor": [
    255,
    255,
    255
  ]
}"""
    with open('assets/picklenicker.json', 'w') as file:
        file.write(picklnickerjsontemplate)
with open('assets/picklenicker.json', 'r') as file:
    settings = json.load(file)

SW = 1000
SH = 600

def get_picklenicker_json_attributes():
    try:
        with open('assets/picklenicker.json', 'r') as file:
            settings = json.load(file)
        return settings
    except PermissionError as error:
        print(f"Error while fetching settings\n{error}\n")

def set_new_picklenicker_json_attributes(difficulty=None, highscore=None, bgcolor=None):
    settings = get_picklenicker_json_attributes()
    try:
        with open('assets\picklenicker.json', 'w') as file:
            if difficulty:
                settings["difficulty"] = difficulty
            if highscore:
                settings["highscore"] = highscore
            if bgcolor:
                settings["bgcolor"] = bgcolor
            json.dump(settings, file, indent=2)
    except PermissionError as error:
        print(f"Error while setting new settings\n{error}\n")
# _________

skyblue = (135, 206, 235)

screen = pygame.display.set_mode((SW, SH), pygame.RESIZABLE)
pygame.display.set_caption("Picklenicker 1.1 Beta")
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
    def __init__(self, pickle, multiplier, speed, x=None, y=None, deadly=False):
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
        self.deadly = deadly
    
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
        self.maxhp = 10
        self.immune = False
        self.poweredup = False
    
    def squidward(self):
        self.poweredup = True
        self.speed = SW / 50
        self.immune = True
        self.image = assets.squidward
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], assets.squidward.get_width(), assets.squidward.get_height())
    def unsquidward(self):
        self.poweredup = False
        self.speed = SW / 100
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

class Explosion:
    def __init__(self, pos):
        self.timeleft = 100
        self.pos = pos
    def draw(self):
        screen.blit(assets.explosion, self.pos)

keyassign = {
        pygame.K_RIGHT: "right",
        pygame.K_LEFT: "left",
        pygame.K_d: "right",
        pygame.K_a: "left",
        pygame.K_t: "toggle debug",
        pygame.K_b: "stop",
        pygame.K_ESCAPE: "stop",
        pygame.K_p: "pause",
        pygame.K_SPACE: "pause",
        pygame.K_c: "neutralize direction",
        pygame.K_r: "reset lag counter"
}
debug = False

def gen_pickles(pickles, bombs=0):
    pickles_list = []
    for pickle in range(pickles):
        pickles_list.append(
            Pickle(
            random.choice(assets.pickles),
            random.randint(50, 100) / 60,
            random.randint(2, 4)
            )
        )
    for bomb in range(bombs):
        pickles_list.append(
            Pickle(
            assets.bomb,
            random.randint(50, 100) / 60,
            random.randint(2, 4),
            deadly=True
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

def run():
    # delete the python cache, as it can cause many problems
    import shutil
    try:
        if "__pycache__" in os.listdir():
            shutil.rmtree("__pycache__")
            print("Successfully deleted the __pycache__ (python cache) folder")
    except OSError as error:
        print(f"Error encountered when deleting the python cache:\n{error}")
    
    explosions = []

    schrodinger = assets.schrodinger
    global debug
    global SW
    global SH

    difficulty = get_picklenicker_json_attributes()["difficulty"]
    buttonplay = pygame.Rect(200, 300, 128, 70)
    running = True
    playtext = font.render("PLAY", True, (50, 50, 50))
    smallfont = assets.smallfont
    difficultyfont = assets.largefont
    title = assets.titlefont.render("PICKLENICKER", True, (50, 50, 50))
    difficultytitle = smallfont.render("Difficulty:", True, (50, 50, 50))
    clicktochangetext = smallfont.render("Click to change", True, (50, 50, 50))

    bgcolorttitle = smallfont.render("Current game background color", True, (0, 0, 0))
    bgcolortext_clicktochange = smallfont.render("Click here to randomize (or q)", True, (0, 0, 0))
    
    development_notes = smallfont.render("Color choosing development in progress!", True, (0,
                                                                                           0,
                                                                                           0))
    while running:
        bgcolor_rect = pygame.Rect(5, 465, 375, 65)
        difficultytext = difficultyfont.render(difficulty, True, (50, 50, 50))
        difficultyhitbox = pygame.Rect(490, 340, difficultytext.get_width() + 20, 141)
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
                if event.key == pygame.K_1:
                    difficulty = "easy"
                if event.key == pygame.K_2:
                    difficulty = "normal"
                if event.key == pygame.K_3:
                    difficulty = "hard"
                if event.key == pygame.K_0:
                    difficulty = "HACKED!!!"
                if event.key == pygame.K_q:
                    set_new_picklenicker_json_attributes(bgcolor=(random.randint(0, 255), 
                                                                  random.randint(0, 255), 
                                                                  random.randint(0, 255)))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonplay.collidepoint(mousepos[0], mousepos[1]):
                    running = False
                if difficultyhitbox.collidepoint(mousepos[0], mousepos[1]):
                    if difficulty == "normal":
                        difficulty = "hard"
                    elif difficulty == "hard":
                        difficulty = "easy"
                    elif difficulty == "easy":
                        difficulty = "normal"
                if bgcolor_rect.collidepoint(mousepos[0], mousepos[1]):
                    set_new_picklenicker_json_attributes(bgcolor=(random.randint(0, 255), 
                                                                  random.randint(0, 255), 
                                                                  random.randint(0, 255)))
            if event.type == pygame.VIDEORESIZE:
                SW, SH = event.size
            
        if buttonplay.collidepoint(mousepos[0], mousepos[1]):
            buttonplayimage = assets.button_overlay_hovered
        else:
            buttonplayimage = assets.button_overlay
        screen.fill(skyblue)
        screen.blit(pygame.transform.rotate(buttonplayimage, math.sin(time.time()) * 10), (200, 300))
        screen.blit(pygame.transform.rotate(playtext, math.sin(time.time()) * 10), (210, 310))
        screen.blit(title, (20, 50))
        pygame.draw.rect(screen, (255, 255, 255), difficultyhitbox)
        pygame.draw.rect(screen, get_picklenicker_json_attributes()["bgcolor"], bgcolor_rect)
        screen.blit(difficultytitle, (500, 350))
        screen.blit(difficultytext, (500, 370))
        screen.blit(clicktochangetext, (500, 445))

        screen.blit(bgcolorttitle, (10, 470))
        screen.blit(bgcolortext_clicktochange, (10, 500))
        screen.blit(development_notes, (0, 580))

        if pygame.key.get_pressed()[pygame.K_j]:
            screen.blit(assets.walrus, (0, 0))

        pygame.display.update()

    set_new_picklenicker_json_attributes(difficulty)

    if difficulty == "hard":
        num_of_bombs = 1
    else:
        num_of_bombs = 0
    difficulties_pickles = {"easy": 3,
                            "normal": 5,
                            "hard": 10,
                            "HACKED!!!": 50}
    pickles = gen_pickles(difficulties_pickles[difficulty], num_of_bombs)

    powerup = WWW()

    
    player = Player(assets.player)
    if difficulty == "HACKED!!!":
        player.maxhp = 1000
        player.hp = 1000

    x = player.x
    y = player.y

    score = 0

    todo = []
    tickengine = pygame.time.Clock()

    speed = 0

    squidwardtime = 0

    bgcolor = get_picklenicker_json_attributes()["bgcolor"]

    timewhenstarted = time.time()
    tickscompleted = 0
    reseted_lag_counter = False
    tickrate = 100
    while True:
        if player.hp <= 0:
            try:
                if score > get_picklenicker_json_attributes()["highscore"]:
                    set_new_picklenicker_json_attributes(highscore=score)
            except PermissionError as error:
                print(f"Error when assigning highscore:\n{error}\nThis is normal. You can change your high score manually by going into pn1.1/assets/picklenicker.json")
                pass
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
                try:
                    highscore = get_picklenicker_json_attributes()["highscore"]
                    highscorestr = font.render(f"High score: {str(highscore)}", True, (255, 0, 0))
                except PermissionError:
                    print(f"Error when reading highscore:\n{error}\nThis is normal. You can read your high score manually by going into pn1.1/assets/picklenicker.json")
                    pass
                screen.blit(youdied, (30, 30))
                screen.blit(scorestr, (30, 200))
                screen.blit(highscorestr, (30, 280))

                pygame.display.update()

        # TPS boosting {
        todo = list(set(todo))
        # }
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
            if item == "reset lag counter":
                timewhenstarted = time.time()
                tickscompleted = 0
                reseted_lag_counter = True
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
                        if event.type == pygame.VIDEORESIZE:
                            SW, SH = event.size
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_b:
                                pygame.quit()
                                sys.exit()
                            if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                                paused = False
            if item == "neutralize direction":
                player.direction = None

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
        screen.fill(bgcolor)
        for pickle in pickles:
            if pickle.x + pickle.width < 0 or pickle.x > SW:
                pickle.draw([random.randint(0, SW - pickle.width), 0 - random.randint(300, 600)])
            if pickle.y > SH:
                pickle.draw([random.randint(0, SW - pickle.width), 0 - random.randint(300, 600)])
                if not player.immune and not pickle.deadly:
                    player.hp -= 1
            if hitbox_intersect(player.hitbox, pickle.hitbox):
                score += pickle.width
                if pickle.deadly:
                    if not player.poweredup:
                        player.hp -= 2
                        explosions.append(Explosion((pickle.x, player.y)))
                pickle.draw([random.randint(0, SW - pickle.width), 0 - random.randint(300, 600)])
            pickle.draw([pickle.x, pickle.y + pickle.speed])
        
        for explosion in explosions:
            if explosion.timeleft <= 0:
                explosions.remove(explosion)
            explosion.timeleft -= 1
            explosion.draw()
        
        powerup.draw([powerup.x, powerup.y + 1])
        if hitbox_intersect(player.hitbox, powerup.hitbox):
            powerup.draw([random.randint(0, SW - powerup.width), 0 - random.randint(600, 1600)]) # if you dont eat the powerup, you lose it forever... intentional
            squidwardtime += 600
        if powerup.y > SH:
            powerup.draw([random.randint(0, SW - pickle.width), 0 - random.randint(300, 600)])

        # render hp
        penx = 0
        peny = 0
        for i in range(player.hp):
            screen.blit(assets.heart, (penx, peny))
            penx += 16
            if penx >= SW:
                penx = 0
                peny += 16
        for i in range(player.maxhp - player.hp):
            screen.blit(assets.noheart, (penx, peny))
            penx += 16
            if penx >= SW:
                penx = 0
                peny += 16
        # render score
        scorestr = font.render(str(score), True, (255, 0, 0))
        screen.blit(scorestr, (SW - scorestr.get_width(), 0))

        if squidwardtime:
            player.squidward()
        else:
            player.unsquidward()
        player.draw([x, y])

        if squidwardtime > 0:
            squidwardtime -= 1
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 20, squidwardtime / 4, 32))
            screen.blit(assets.powerup_squidward, (0, 20)) # i put a comment here for no reason at all, again

        keyspressed = pygame.key.get_pressed()
        if keyspressed[pygame.K_j]:
            screen.blit(assets.walrus, (0, 0))
        if keyspressed[pygame.K_s]:
            screen.blit(schrodinger, (0, 0))
        if debug:
            currentticklag = ((time.time() - timewhenstarted) - tickscompleted / 100)
            seconds_lagged_string_end_dict = {False: "since start",
                                            True: "since last restart"}
            lagtextoverall = smallfont.render(f"Seconds lagged: {round(currentticklag, 5)} seconds {seconds_lagged_string_end_dict[reseted_lag_counter]}",
                                            True, (50, 50, 50))
        if debug:
            if squidwardtime:
                debugpen_y = 52
            else:
                debugpen_y = 20
            screen.blit(lagtextoverall, (0, debugpen_y))
        pygame.display.update()
        tickengine.tick(int(tickrate))
        tickrate
        tickscompleted += 1
#%% end
while True:
    if run() == "dead":
        pass