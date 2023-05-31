import pygame
from enum import Enum
from settings import *


class Positions(Enum):
    ALLY_FRONT = 0
    ALLY_TOP = 1
    ALLY_BOTTOM = 2
    ENEMY_FRONT = 3
    ENEMY_TOP = 4
    ENEMY_BOTTOM = 5
    ENEMY_BOSS = 6

positions_list = [
    (630, 525),
    (300, 300),
    (300, 730),
    (1290, 525),
    (1620, 300),
    (1620, 730),
    (1415, 530)
]

# In order: Small, Medium, Big, Boss
size_list = [(150,125), (300,250), (360,300), (550,450)]

class Character:
    allyCount = 0
    enemyCount = 3
    updated_positions_list = []

    def __init__(self, imgpath: str, size = "medium", ally= True , bossSize = False):
        self.img = pygame.image.load("images/characters/"+imgpath).convert_alpha()
        self.ally = ally
        self.size = self.findSize(size)
        if bossSize: self.size = size_list[3]
        # Scales images while keeping the same width-height ratio, Height is shared for everyone (250 or size[1])
        # while Width is changed depending on how much Height was changed
        self.sprite_size = (self.img.get_width() * (self.size[1]/self.img.get_height()), self.size[1])
        self.img = pygame.transform.scale(self.img, self.sprite_size)
        self.draw_offset = (self.size[0] - self.sprite_size[0])/2
        if ally:
            self.pos = positions_list[Character.allyCount]
            Character.allyCount += 1
            self.img = pygame.transform.flip(self.img, True, False)
        else:
            self.pos = positions_list[Character.enemyCount]
            if bossSize:    self.pos = positions_list[Positions.ENEMY_BOSS.value]
            Character.enemyCount += 1
        Character.updated_positions_list.append(self.pos)

        self.maxHp = 200
        self.hp = self.maxHp
        self.atk = 80
        self.out_of_combat = False
        self.hpBarSurface = self.createHpBarSurface()
        self.rect = self.img.get_rect(center=self.pos)


    def getRect(self):
        return self.rect

    def getSprite(self):
        return self.img

    def getPos(self):
        return self.pos[0] + self.draw_offset, self.pos[1]

    def createHpBarSurface(self):
        # Creates a pygame surface to draw the hpBar on
        surface = pygame.Surface((self.size[0], 30)).convert_alpha()
        surface.fill([0, 0, 0, 0]) # Transparent surface background
        pygame.draw.rect(surface, "#4f0f0f", pygame.Rect(5, 5, self.size[0]-10, 20), 0, 3)
        pygame.draw.rect(surface, "red", pygame.Rect(5, 5, self.size[0]*(self.hp/self.maxHp)-10, 20))
        pygame.draw.rect(surface, "white", pygame.Rect(0, 0, self.size[0], 30), 5, 8)

        return surface

    def getHpBarSurface(self):
        return self.createHpBarSurface()

    def getHpBarRect(self):
        return self.hpBarSurface.get_rect(midtop = (self.rect.midbottom[0], self.rect.midbottom[1] + 15))

    def takeDamage(self, dmg: int):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def attackOther(self, defender):
        defender.takeDamage(self.atk)

    def die(self):
        Character.updated_positions_list.remove(self.pos)
        self.hp = 0
        self.out_of_combat = True

    def isDead(self):
        return self.out_of_combat

    def getOffset(self):
        return self.draw_offset

    def findSize(self, size_str):

        if size_str == "small":
            return size_list[0]
        elif size_str == "medium":
            return size_list[1]
        elif size_str == "big":
            return size_list[2]
        elif size_str == "boss":
            return size_list[3]
        else:
            print(f"wrong size parameter for {self}")
            return size_list[1]
