import pygame
from typing import Tuple, List
from characters import *
from ui import BattlePointerArrow
from settings import *

class Battle:
    def __init__(self, game, allies: List, enemies: List):
        # Loads useful game vars
        self.GAME = game
        self.char_data = self.GAME.characters_data

        # Loads combat images
        self.background_image = pygame.image.load("images/backgrounds/BG_cavelake.png")
        self.background_image = pygame.transform.scale(self.background_image, SCREEN_SIZE)

        # Creates team lists
        self.battlers_list, self.allyTeam, self.enemyTeam = [], [], []
        # Add Characters instances to lists using json data
        self.generateTeams(allies, enemies)

        # Creates pointer arrow ui
        self.pointer_arrow = BattlePointerArrow(self)

        self.turn_counter = 1
        self.state = "selecting_ally"
        self.attacker = None
        self.defender = None


    def draw(self):
        # Draw background
        self.GAME.screen.blit(self.background_image, (0, 0))
        # Draw char sprite and health bar below
        for c in self.allyTeam:
            self.GAME.screen.blit(c.getSprite(), (c.getRect()))
            self.GAME.screen.blit(c.getHpBarSurface(), c.getHpBarRect())
            if self.GAME.debug_mode:
                rect = pygame.Rect(c.getPos()[0], c.getPos()[1], c.getSprite().get_width(), c.getSprite().get_height())
                pygame.draw.rect(self.GAME.screen, 'red', rect, 5)
        for c in self.enemyTeam:
            self.GAME.screen.blit(c.getSprite(), (c.getRect()))
            self.GAME.screen.blit(c.getHpBarSurface(), c.getHpBarRect())
            if self.GAME.debug_mode:
                rect = pygame.Rect(c.getPos()[0], c.getPos()[1], c.getSprite().get_width(), c.getSprite().get_height())
                pygame.draw.rect(self.GAME.screen, 'red', rect, 5)

        # Draws pointer arrow
        if not self.state == "enemy_turn":
            self.GAME.screen.blit(self.pointer_arrow.getImg(), self.pointer_arrow.getPosWithOffset())

        if self.GAME.debug_mode:
            for p in positions_list:
                pygame.draw.rect(self.GAME.screen, 'red', pygame.Rect(p[0],p[1], 5,5))

    # Generates teams lists from arguments and using Game's characters data
    def generateTeams(self, allies, enemies):
        for name in allies:
            char = None
            # Loops over every character data from json until finding one with matching name(str) or id(int)
            for c in self.char_data:
                if name == c["name"] or name == c["id"]:
                    char = Character(c["filename"], c["size"], True)
                    self.allyTeam.append(char)

        # Enemy is a boss if argument isn't a list
        if isinstance(enemies, str) or isinstance(enemies, int):
            for c in self.char_data:
                if enemies == c["name"] or enemies == c["id"]:
                    char = Character(c["filename"], c["size"], False, True)
                    self.enemyTeam.append(char)
        else:
            for name in enemies:
                char = None
                for c in self.char_data:
                    if name == c["name"] or name == c["id"]:
                        char = Character(c["filename"], c["size"], False)
                        self.enemyTeam.append(char)

        self.battlers_list = self.allyTeam + self.enemyTeam

    def damageCharacter(self, char, dmg: int):
        char.takeDamage(dmg)
        self.checkForDeaths()


    def damageTeam(self, team, dmg: int):
        for c in team:
            self.damageCharacter(c, dmg)

    def checkForDeaths(self):
        for char in self.battlers_list:
            if char.isDead():
                self.battlers_list.remove(char)
                if char.ally == True:
                    self.allyTeam.remove(char)
                if char.ally == False:
                    self.enemyTeam.remove(char)

    def update(self):
        pass

    def nextActionState(self):
        if self.state == "selecting_ally":
            self.attacker = self.getTargetedCharacter()
            self.pointer_arrow.max_len = len(self.battlers_list)
            self.state = "selecting_enemy"
        elif self.state == "selecting_enemy":
            self.defender = self.getTargetedCharacter()
            self.attacker.attackOther(self.defender)
            self.checkForDeaths()
            self.state = "enemy_turn"
        elif self.state == "enemy_turn":
            self.damageTeam(self.allyTeam, 5)
            self.pointer_arrow.max_len = len(self.allyTeam)
            self.state = "selecting_ally"


    def getTargetedCharacter(self):
        return self.battlers_list[self.pointer_arrow.getPosIndex()]